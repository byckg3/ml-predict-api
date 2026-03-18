import chromadb
import pandas as pd

class ChromaDB:

    def __init__( self, path: str, name: str, embed_function = None, is_persistent: bool = False ):

        if is_persistent:
            self.client = chromadb.PersistentClient( path )
        else:
            self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection( name = name,
                                                                embedding_function = embed_function )
        print( "\nCreate ChromaDB connection successfully" )

    def load( self, n_records = -1 ):

        qa_data_df = pd.read_parquet( "./data/qa.parquet", engine = "pyarrow" )
        heart_disease_df = pd.read_parquet( "./data/heart_disease.parquet", engine = "pyarrow" )
        liver_disease_df = pd.read_parquet( "./data/liver_disease.parquet", engine = "pyarrow" )

        self.add( qa_data_df, n_records )
        self.add( heart_disease_df, n_records )
        self.add( liver_disease_df, n_records )

        if self.ping():
            print( "parquet data loaded successfully" )
        else:
            print( "parquet data loading failed" )

    def add( self, df, n_records = -1 ):
        
        n = df.shape[ 0 ]
        if n_records >= 0:
            n = min( n, n_records )

        embeddings = df[ "embedding" ].tolist()[ :n ]
        documents = df[ "document" ].tolist()[ :n ]
        ids = df[ "id" ].tolist()[ :n ]
        metadatas = df.drop( columns = [ "id", "document", "embedding" ] ).to_dict( orient = "records" )[  :n ]

        self.collection.upsert(
                documents = documents,
                embeddings = embeddings,
                ids = ids,
                metadatas = metadatas,
        )
    
    def ping( self ):
        try:
            result = self.collection.get( limit = 1 )
            if result:
                return True
            
        except Exception as e:
            print( e )

        return False