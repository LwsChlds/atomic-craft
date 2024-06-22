import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from database import Database
from fastapi.middleware.cors import CORSMiddleware
from data_processing import get_compound_components

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database()
db.setup_tables()


class Combination(BaseModel):
    data: dict


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/combine")
async def combine(combinations: Combination):
    elements = {}
    for key, value in combinations.data.items():
        isolated_values = get_compound_components(key)
        isolated_values.update({n: isolated_values[n] * value for n in isolated_values.keys()})
        for element, count in isolated_values.items():
            elements[element] = elements.get(element, 0) + count
    find_combinations = db.find_prompt(elements)
    if not find_combinations:
        return {"success": False, "creates": {}}
    response = {"name": find_combinations[1],
                "equation": find_combinations[2]}
    return {"success": True,
            "creates": response}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)