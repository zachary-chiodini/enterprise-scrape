'''
+------------------------------------+
|           html_tools.py            |
+------------------------------------+
| Extract Data From HTML Source Code |
+------------------------------------+
'''
from typing import List, Tuple

def clean( html : str, left : str, right : str ) -> str :
    ''' 
    Remove Text between Characters Left and Right
    '''
    rslt = ''
    strt, stop = 0, 0
    for i in range( len( html ) ) :
        if html[ i ] == left :
            stop = i
            continue
        if html[ i ] == right :
            rslt += html[ strt : stop ]
            strt = i + 1
    return rslt if rslt else html

def incrAndComp( html : str, i : int, j : int, stng : str ) -> Tuple[ int, bool ] :
    ''' 
    Increment i and Incrementally Compare html with stng 
    '''
    while j < len( stng ) and i + j < len( html ) :
        if html[ i + j ] != stng[ j ] :
            return j, False
        j += 1
    return j, True

def decrAndComp( html : str, k : int, h : int, stng : str ) -> Tuple[ int, bool ] :
    ''' 
    Decrement k and Decrementally Compare html with stng 
    '''
    while h >= -len( stng ) + 1 :
        if html[ k + h ] != stng[ h - 1 ] :
            return h, False
        h -= 1
    return h, True
    
def abstract( html : str, left : str, right : str ) -> List[ str ] :
    '''
    Returns List of Strings Found Preceding Right and
    the First Encounter of Left
    '''
    rslt = []
    i, j = 0, 0
    while i < len( html ) :
        if html[ i ] == right[ j ] :
            j, same = incrAndComp( html, i, 1, right )
            if same :
                stop = i + j - len( right ) - 1
                k = stop
                lim = k - 100 # limit of decrementation
                while k >= lim and k >= 0 :
                    if html[ k ] == left[ -1 ] :
                        h, same = decrAndComp( html, k, -1, left )
                        if same :
                            exct = html[ k + 1 : stop ]
                            rslt.append( exct )
                            break
                    k -= 1
        i += j + ( not bool( j ) )
        j = 0
    return rslt
    
def extract( html : str, left : str, right : str, 
             onetime : bool = False, scrub : bool = False ) -> List[ str ] :
    '''
    Returns List of Strings Found Between Left and Right Tags
    '''
    rslt = []
    i, j, strt = 0, 0, 0
    # single pass O(n) amortized
    while i < len( html ) :
        if html[ i ] == left[ 0 ] :
            j, same = incrAndComp( html, i, 1, left )
            if same :
                if left == right :
                    if not strt :
                        strt = i + j
                        i += j + ( not bool( j ) )
                        j = 0
                        continue
                    else :
                        j = 0
                else :
                    strt = i + j
        if j < len( right ) and html[ i + j ] == right[ j ] :
            j, same = incrAndComp( html, i, j + 1, right )
            if same and strt :
                exct = html[ strt : i ]
                strt = 0
                if exct :
                    if onetime :
                        rslt.append( exct )
                        break
                    if scrub :
                        exct = clean( exct + '<>', '<', '>' )
                        rslt.append( exct.strip() )
                    else :
                        rslt.append( exct.strip() )
        i += j + ( not bool( j ) )
        j = 0
    return rslt

def extractMail( html : str ) -> List[ str ] :
    email = []
    i, j, k = 0, 0, 0
    while i < len( html ) :
        if html[ i ] == '@' :
            j, k = i, i
            while ( 
                ( j >= 0 and k < len( html ) ) and
                ( html[ j ] != ' ' or html[ k ] != ' ' ) 
                ) :
                if html[ j ] != ' ' :
                    j -= 1
                if html[ k ] != ' ' :
                    k += 1
            email.append( 
                html[ j + 1 : k ].strip( '.' ).strip( ';' )\
                    .strip( ',' ).strip( '<' ).strip( '>' )
                )
        i += 1
    return email