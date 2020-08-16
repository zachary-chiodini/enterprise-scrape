<table align="left">
    <tr>
        <td colspan="3">
            <img src="python.png" style="width:20%; height:20%" align="left"/>
        </td>
    </tr>
    <tr>
        <td><span style="font-family:cambria; font-size:40px">Enterprise Scrape API</span></td>
        <td><span style="font-family:cambira; font-size:40px">&nbsp;|</span></td>
        <td><span style="font-family:cambira; font-size:24.7px"><i>Scrape Enterprise Data from Google</i></span></td>
    </tr>
    <tr>
        <td colspan="3"><hr></td>
    </tr>
</table>

```python
from enterprise_scrape import Scrape
```

<hr>
<i style="font-size:15.9px">Send a query to Google and extract the search results from the souce code::</i>
<hr>


```python
scrape = Scrape()
scrape.google( 'ibm company' )
scrape.getResult()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Source</th>
      <th>Links</th>
      <th>Summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>https://www.ibm.com</td>
      <td>ibm - united states</td>
      <td>for more than a century ibm has been dedicated...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>https://www.ibm.com</td>
      <td>about ibm - united states</td>
      <td>collectively, they have fostered some of the c...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>https://en.wikipedia.org</td>
      <td>ibm - wikipedia</td>
      <td>website. ibm.com. international business machi...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>https://www.cbronline.com</td>
      <td>what is ibm? - computer business review</td>
      <td>international business machines (ibm), is a gl...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>https://www.linkedin.com</td>
      <td>ibm | linkedin</td>
      <td>ibm is a leading cloud platform and cognitive ...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>https://www.britannica.com</td>
      <td>ibm | founding, history, &amp;amp; products | brit...</td>
      <td>ibm (international business machines corporati...</td>
    </tr>
    <tr>
      <th>6</th>
      <td>https://money.cnn.com</td>
      <td>ibm - international business machines corp com...</td>
      <td>the company was founded by charles ranlett fli...</td>
    </tr>
    <tr>
      <th>7</th>
      <td>https://searchitchannel.techtarget.com</td>
      <td>what is ibm? - definition from whatis.com - se...</td>
      <td>ibm is a global information technology company...</td>
    </tr>
    <tr>
      <th>8</th>
      <td>https://finance.yahoo.com</td>
      <td>international business machines (ibm) company ...</td>
      <td>international business machines corporation op...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>https://www.bloomberg.com</td>
      <td>international business machines corp - company...</td>
      <td>international business machines corporation (i...</td>
    </tr>
  </tbody>
</table>
</div>



<hr>
<i style="font-size:15.9px">Extract Information from Google's information box, if one exists:</i>
<hr>


```python
scrape.getBox()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>wiki</th>
      <td>international business machines corporation is...</td>
    </tr>
    <tr>
      <th>ceo</th>
      <td>arvind krishna (apr 6, 2020–)</td>
    </tr>
    <tr>
      <th>customer service</th>
      <td>1 (877) 426-6006</td>
    </tr>
    <tr>
      <th>sales</th>
      <td>1 (888) 746-7426</td>
    </tr>
    <tr>
      <th>headquarters</th>
      <td>armonk, ny</td>
    </tr>
    <tr>
      <th>founder</th>
      <td>charles ranlett flint</td>
    </tr>
    <tr>
      <th>subsidiaries</th>
      <td>red hat software, ibm india private limited, w...</td>
    </tr>
  </tbody>
</table>
</div>



<hr>
<i style="font-size:15.9px">Find alternative names for the company, if they exist:</i>
<hr>


```python
scrape.assocComp( 'ibm' )
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Company Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>international business machines corp</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ibm</td>
    </tr>
    <tr>
      <th>2</th>
      <td>international business machines</td>
    </tr>
  </tbody>
</table>
</div>


