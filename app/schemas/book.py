from pydantic import BaseModel, ConfigDict, Field


class Author(BaseModel):
    fName: str = Field(min_length=3, max_length=50)
    lName: str = Field(min_length=3, max_length=50)
    bio: str = Field(min_length=10, max_length=2000)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "fName": "Madan",
                "lName": "Mohan",
                "bio": "Madan Mohan is Supreme Personality of Godhead.",
            }
        }
    )


class BookCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=10, max_length=20000)
    rating: float = Field(ge=0, le=5)
    author: Author

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Bhagavad-gita As It Is",
                "description": "Srila Prabhupada's translation and commentary on the Bhagavad-gita.",
                "rating": 5.0,
                "author": {
                    "fName": "Srila",
                    "lName": "Prabhupada",
                    "bio": "Founder-acharya of ISKCON and translator of the Bhagavad-gita.",
                },
            }
        }
    )
