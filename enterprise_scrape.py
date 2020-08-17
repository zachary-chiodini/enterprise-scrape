import html_tools as html
import urllib, pandas as pd
from typing import List, Set, Tuple

class Scrape :
    '''
    Scrape Enterprise Data from Google
    '''
    def __init__( self : object ) :
        self.rslts = 10
        self.__box = ''
        self.__source = ''
        
    def getSource( self : object ) -> str :
        return self.__source
    
    def getResult( self : object ) -> pd.DataFrame :
        '''
        Returns DataFrame of Query Results
        '''
        if not self.__box : self.__extractBox()
        data = { 
            'Source' : pd.Series( self.__sites() ),
            'Links'  : pd.Series( self.__links() ),
            'Summary': pd.Series( self.__dscrb() )
        }
        return pd.DataFrame( data )
    
    def getBox( self : object ) -> pd.DataFrame :
        '''
        Returns DataFrame of Data in Side Box
        '''
        if not self.__box : self.__extractBox()
        if self.__box == 'NA' : return pd.DataFrame()
        tags = '<div class="bneawe s3v9rd ap7wnd">', '</div>'
        text = html.extract( self.__box, *tags, scrub = True )
        data = {}
        data[ 'wiki' ] = pd.Series( [ text[ 0 ][ : -13 ] ] )
        for i in range( 1, len( text ) ):
            if ':' in text[ i ] :
                key, val = text[ i ].split( ':' )
                data[ key ] = pd.Series( [ val.strip() ] )
            else :
                break
        df = pd.DataFrame( data ).transpose()
        df.columns = [ 'Info' ]
        return df

    def getReview( self : object, name : str ) -> pd.DataFrame :
        '''
        Find Average Review of Company Name
        '''
        self.google( '{} reviews'.format( name ) )
        # get sources
        srce = []
        tags = '<div class="bneawe upmit ap7wnd">', '<span class="r0bn4c rqmqod">rating</span>'
        for scrp in html.extract( self.__source, *tags, scrub = True ) :
            for i in range( len( scrp ) ) :
                if scrp[ i ] == '›' :
                    srce.append( scrp[ 0 : i - 1 ] )
                    break
        tags = '<span class="r0bn4c rqmqod">rating</span>', ')</span>'
        digits = 0
        totrates = 0
        allrates, allvotes = [], []
        for review in html.extract( self.__source, *tags, scrub = True ) :
            rating, votes = review.split()
            rating = rating.strip()
            votes = float( votes.strip( '()' ).replace( ',', '' ) )
            for i in range( len( rating ) ) :
                if rating[ i ] == '.' :
                    n = len( rating[ i + 1 : ] )
                    if not digits or n < digits :
                        digits = n
                    break
            totrates += float( rating ) * votes
            allvotes.append( votes )
            allrates.append( float( rating ) )
        df = pd.DataFrame({ 
            'Source' : pd.Series( srce ),
            'Votes'  : pd.Series( allvotes ),
            'Avg Rating' : pd.Series( allrates )
            })
        tot = pd.DataFrame({
            'Source' : [''],
            'Votes'  : [''],
            'Avg Rating' : [ round( totrates / sum( allvotes ), digits ) 
                            if sum( allvotes ) else '' ]
            })
        tot.index = [ 'Total' ]
        return pd.concat( [ df, tot ], axis = 0 )

    def getEmail( self : object, name : str ) -> pd.DataFrame :
        '''
        Find Emails Related to Company Name
        '''
        email = []
        self.google( '{} emails'.format( name ) )
        tags = ' ', '@<span class="fcup0c rqmqod">'
        mailbox = html.abstract( self.__source, *tags )
        tags = '@<span class="fcup0c rqmqod">', '</div>'
        domain = html.extract( self.__source, *tags, scrub = True )
        for mail, dom in zip( mailbox, domain ) :
            email.append( mail + '@' + dom.strip( '.' )  )
        if not email :
            spcl = { '$', '%', '#', '/', '\\', '<', '>', '!', '^',
                     '(', ')', '|', '{',  '}', ':', '[', ']', ';' }
            tags = '<div class="bneawe s3v9rd ap7wnd">', '</div>'
            for text in html.extract( self.__source, *tags, scrub = True ) :
                for mail in html.extractMail( text ) :
                    if any( char in mail for char in spcl ) :
                        continue
                    else :
                        email.append( mail )
        return pd.DataFrame( { 'Email' : pd.Series( email ) } )
        
    def assocComp( self : object, name : str ) -> pd.DataFrame :
        '''
        Returns List of Companies Associated with Company Name
        '''
        def extractName( link : str ) -> str :
            '''
            Extracts Company Name from Link
            '''
            name = ''
            for key in bank :
                if key in link :
                    link = link.split( key )[ 0 ]
                    name = link
                    for char in special :
                        if char in link :
                            link = link.split( char )[ 0 ]
                            name = link
                            break
                    break
            return name
        special = [ '|', ' - ', ' -', '- ', '...',   '®',
                    '–',   '—',  ';',  ':',   '»', '.,.' ]
        bank = [
                  'aljazeera',   'bloomberg', 'business profile', 'business profiles',
            'company profile', 'company profiles',  'craigslist',        'crunchbase',     
                   'facebook',       'forbes',       'glassdoor',            'indeed', 
               'investopedia',     'linkedin',         'monster',             'owler',      
                    'reviews',      'twitter',         'usajobs',         'wikipedia',        
                      'yahoo', 'ziprecruiter',        'zoominfo'
        ]
        comps = { name }
        self.google( '{} company'.format( name ) )
        for link in self.__links() :
            comp = extractName( link )
            if comp :
                comp = html.clean( comp, '(', ')' )
                comps.add( comp.strip() )
        comps = [ n for n in comps ]
        return pd.DataFrame( { 'Company Name' : comps } )
    
    def parentComp( self : object, name : str ) -> pd.DataFrame :
        '''
        Returns List of Company Name's Parent Companies
        '''
        self.google( '{} parent company'.format( name ) )
        self.__extractBox()
        tags = '<div class="bneawe s3v9rd ap7wnd">\
<div class="ap5osd"><div class="bneawe s3v9rd ap7wnd">\
<span class="fcup0c rqmqod">', '</span>'
        prnt = html.extract( self.__source, *tags )
        if not prnt :
            tags = '<div class="bneawe ibp4i ap7wnd">', '</div>'
            prnt = html.extract( self.__source, *tags )
        if not prnt :
            tags = '<div class="rwuggc kcryt"><div><div class="bneawe s3v9rd ap7wnd">',\
                   '</div>'
            prnt = html.extract( self.__source, *tags )
        return pd.DataFrame( { 'Parent Company' : prnt } )
    
    def childComp( self : object, name : str ) -> List[ str ] :
        '''
        Returns List of Company Name's Child Companies
        '''
        self.google( '{} subsidiary'.format( name ) )
        self.__extractBox()
        self.__extractMore()
        tags = '<div class="rwuggc kcryt"><div><div class="bneawe s3v9rd ap7wnd">',\
               '</div>'
        child = html.extract( self.__source, *tags )
        if not child :
            tags = '<div class="am3qbf"><div><span><div class="bneawe deivcb ap7wnd">',\
                   '</div>'
            child = html.extract( self.__source, *tags )
        if not child :
            tags = '<div class="bneawe ibp4i ap7wnd">', '</div>'
            child = html.extract( self.__source, *tags )
        if not child :
            tags = '<div class="bneawe s3v9rd ap7wnd">\
<div class="ap5osd"><div class="bneawe s3v9rd ap7wnd">\
<span class="fcup0c rqmqod">', '</span>'
            child = html.extract( self.__source, *tags )
        return pd.DataFrame( { 'Subsidiary' : child } )
        
    def google( self : object, query : str ) -> None :
        '''
        Request Google Query
        '''
        query = query.replace( ' ', '+' )
        url = 'https://www.google.com/search?q={}&num={}'
        self.__request( url.format( query, self.rslts ) )
        return

    def __extractMore( self : object ) -> None :
        '''
        Extract Unnecessary Text from Bottom of Page
        '''
        tags = 'related searches', 'sign in'
        more = html.extract( self.__source, *tags, onetime = True )
        if more :
            self.__source = self.__source.replace( more[ 0 ], '' )
        return
    
    def __extractBox( self : object ) -> None :
        '''
        Extracts Side Box from Source Code.
        '''
        tags = '<div class="zinbbc xpd o9g5cc uupgi"><div class="kcryt"><div class="ngphre">',\
               'people also ask'
        box = html.extract( self.__source, *tags, onetime = True )
        if box :
            self.__box = box[ 0 ]
            self.__source = self.__source.replace( self.__box, '' )
        else :
            self.__box = 'NA'
        return
        
    def __links( self : object ) -> List[ str ] :
        '''
        Get List of Queried Links 
        '''
        tags = '<div class="bneawe vvjwjb ap7wnd">', '</div>'
        return html.extract( self.__source, *tags )
    
    def __dscrb( self : object ) -> List[ str ] :
        '''
        Get Summary of Each Link
        '''
        if not self.__box : self.__extractBox()
        tags = '<div class="bneawe s3v9rd ap7wnd">', '</div>'
        return html.extract( self.__source, *tags, scrub = True )
    
    def __sites( self : object ) -> List[ str ] :
        '''
        Get the URL of Each Link
        '''
        tags = '<div class="bneawe upmit ap7wnd">', '›'
        return html.extract( self.__source, *tags )
        
    def __request( self : object, url : str ) -> None :
        '''
        Request URL and Return HTML Source Code
        '''
        req = urllib.request.Request( 
            url, headers = { 'User-Agent' : 'Mozilla/5.0' } 
        )
        self.__source = urllib.request.urlopen( req )\
            .read().decode( 'UTF-8', 'ignore' ).lower()
        return