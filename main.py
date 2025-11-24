from fastapi import FastAPI,Form,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor
from database import get_connection
from deepface import DeepFace
import psycopg2,os,models,datetime



app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 allows all domains (use specific domain for security)
    allow_credentials=True,
    allow_methods=["*"],  # 👈 allows all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # 👈 allows all headers
)


@app.post("/login")
def post_req(data: models.Log_in_Data_validation ):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(" SELECT email_id,password,isteacher from user_table where email_id=%s",(data.email,))
    user_detail=cursor.fetchone()
    cursor.close()
    conn.close()

    if data.password==user_detail[1] and user_detail[2]==False:
        return { "success" : True, "is_teacher" : False }
    elif user_detail and data.password == user_detail[1] and user_detail[2]==True:
        return { "success" : True, "is_teacher" : True }
    else:
        return { "success" : False , "is_teacher" : True } # this is for correct email and  wrong password 
    


@app.post("/upload")
async def face_verify(email:str = Form(), file: UploadFile = Form(...)):
    contents = await file.read()
    filename = f"{email.replace('@','_')}.jpg"
    prefDirectory = "uploads"
    full_path = os.path.join(prefDirectory,filename)

    with open (full_path,"wb") as f:
        f.write(contents)

    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("select image_data from user_table where email_id=%s",(email,))
    conn.commit()

    binaryDataOfImage=cursor.fetchone()
    binaryDataOfImage=binaryDataOfImage[0]

    # covert the binary data to jpg file
    filename1=filename
    filename1=filename1.replace(".jpg","1.jpg")
    full_path=os.path.join(prefDirectory,filename1)
    with open(full_path,"wb") as f:
        f.write( binaryDataOfImage)

    cursor.close()
    conn.close()

    # compare two images and return a result["verified"]
    filename="uploads/"+filename
    filename1="uploads/"+filename1

    img1=filename
    img2=filename1

    result = DeepFace.verify(
        img1,
        img2,
        model_name="ArcFace",
        # detector_backend="retinaface"
        
    )
    
    return {"success":result["verified"]}
    
    

@app.post("/verify_qr")
def mark_attendance(data : models.Qrdata):

    conn=get_connection()
    cursor=conn.cursor()
    
    cursor.execute("select name,usn from user_table where email_id=%s" ,(data.email,))
    name_and_usn = cursor.fetchone()

    name = name_and_usn[0]
    usn = name_and_usn[1]

    branch = data.qr_data[7:9]
    sem = data.qr_data[19:20]
    subject=data.qr_data[29:31]
    date=datetime.date.today()
    date = date.strftime("%Y-%m-%d")
    date=date.replace("-","_")
    Schema = "_"+sem+"_"+branch
    table = "_"+date + "_" + subject
    
    cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{Schema}"')

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS "{Schema}"."{table}" (
        reg_no VARCHAR(10) PRIMARY KEY,
        name VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

    conn.commit()

    cursor.execute(f''' insert into "{Schema}"."{table}" (reg_no,name) values (%s,%s)''',(usn,name,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"success":True}


@app.post("/save_qr")
def save_qr_data(qrdata:models.Qrdatavalidation):
    
    return {"success":True,"message":"manual success message"}









