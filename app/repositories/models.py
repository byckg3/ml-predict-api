from huggingface_hub import HfApi, hf_hub_download, login

from app.core.config import hf_settings

class HFModelRepository:

    REPOSITORY_ID = hf_settings().REPOSITORY_ID

    def __init__( self ):

        login( hf_settings().HF_TOKEN )
        self.api = HfApi()

    async def download( self, repo_filepath, dir = "./hf_models" ):

        model_path = hf_hub_download( repo_id = HFModelRepository.REPOSITORY_ID, 
                                      local_dir = dir,
                                      filename = repo_filepath )
        print( "object_location:", model_path )
        
        return model_path