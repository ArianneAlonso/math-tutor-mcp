crear un entorno virtual en la carpeta server:

python -m venv venv

.\venv\Scripts\activate

descargar dependencias con:

pip install -r requirements.txt



hacer correr el servidor con:

cd server
.\venv\Scripts\activate
python server.py

y en una nueva terminal:

cd server
.\venv\Scripts\activate
python api.py

y en una nueva terminal, hacer correr el client con:

cd client

npm i y luego npm run dev