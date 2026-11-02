from database.DB_connect import DBConnect
from model.artista import Artista


class DAO():

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct c.Country
                from customer c
                where c.Country is not null
                order by c.Country
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["Country"])

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllNodes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select distinct a.*
                from album al, track t ,artist a
                where a.ArtistId =al.ArtistId and al.AlbumId =t.AlbumId  """
            cursor.execute(query)

            for row in cursor:
                result.append(Artista(**row))

            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def getBraniPerArtista(idA):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                        select distinct t.TrackId 
                        from album al, track t 
                        where al.ArtistId=%s and al.AlbumId =t.AlbumId  """

        cursor.execute(query, (idA,))
        for row in cursor:
            results.append(row["TrackId"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPlaylistPerArtista(idA):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct p.PlaylistId 
                        from playlist p , playlisttrack pt ,track t,album al 
                        where al.ArtistId=%s and al.AlbumId =t.AlbumId  
                        and t.TrackId =pT.TrackId and pt.PlaylistId =p.PlaylistId 
                                                     """

        cursor.execute(query, (idA,))
        for row in cursor:
            results.append(row["PlaylistId"])

        cursor.close()
        conn.close()
        return results

