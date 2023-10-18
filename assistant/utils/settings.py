from pydantic_settings import BaseSettings
from pydantic import field_validator, FieldValidationInfo
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    sender_email: str = ""
    qonto_client_id: str
    qonto_secret_key: str
    qonto_iban: str
    
    @field_validator("sender_email")
    def get_address(cls, sender_email: str, info: FieldValidationInfo) -> str:
        if sender_email == "" and "smtp_server" in info.data:
            return info.data["smtp_server"]
        return sender_email
    
    class Config:
        # env_file = ".env"
        # env_file_encoding = "utf-8"
        env_prefix = "CHELLA_DIOR_"
    

if __name__ == '__main__':
    settings = Settings()
    print(settings)
