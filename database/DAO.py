from database.DB_connect import DBConnect
from model.artist import Artist
from model.genre import Genre


class DAO():

    @staticmethod
    def getGeneri():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select * from genre g  """

        cursor.execute(query)

        for row in cursor:
            result.append(Genre(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi(genere):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct a.ArtistId , a.Name 
                    from artist a, album al
                    where a.ArtistId = al.ArtistId 
                    and al.AlbumId in ( select distinct AlbumId 
                                        from track
                                        where GenreId = %s) """

        cursor.execute(query, (genere, ))

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(idMap, genere):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ with acquisti as (select distinct i.CustomerId , a.ArtistId 
                                    from invoice i , invoiceline il, artist a , album al, track t
                                    where i.InvoiceId = il.InvoiceId 
                                    and a.ArtistId = al.ArtistId 
                                    and t.AlbumId  = al.AlbumId 
                                    and il.TrackId = t.TrackId 
                                    and t.GenreId = %s)
                    select distinct a1.ArtistID as A1, a2.ArtistID as A2
                    from acquisti a1, acquisti a2
                    where a1.CustomerID = a2.CustomerID
                    and a1.ArtistID > a2.ArtistID  """

        cursor.execute(query, (genere,))

        for row in cursor:
            result.append((idMap[row['A1']], idMap[row['A2']]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPopolarita(idMap, genere):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ select a.ArtistId, sum(i.Quantity) as peso
                    from artist a , album al, track t, invoiceline i 
                    where a.ArtistId = al.ArtistId 
                    and t.AlbumId  = al.AlbumId 
                    and i.TrackId = t.TrackId 
                    and t.GenreId = %s
                    group by a.ArtistId   """

        cursor.execute(query, (genere, ))

        for row in cursor:
            artista = idMap[row['ArtistId']]
            result[artista]=row['peso']

        cursor.close()
        conn.close()
        return result