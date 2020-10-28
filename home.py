from flask import Flask, render_template, request, json, url_for, redirect,send_from_directory, g, session
import os
#from PyPDF2 import PdfFileReader
from werkzeug.utils import secure_filename
from pathlib import Path
import Modelo as Modelo
import time
import re
import jinja2
import ctypes

app = Flask(__name__)
app.config['UPLOAD_FOLDER5'] ='./static/Contratos'
app.config['UPLOAD_FOLDER4'] ='./static/Selfie'
app.config['UPLOAD_FOLDER3'] ='./static/Comprobante'
app.config['UPLOAD_FOLDER2'] ='./static/INEATRAS'
app.config['UPLOAD_FOLDER'] ='./static/INEDELANTE'
app.config['UPLOAD_EXTENSIONS'] = '.pdf', '.png' , '.jpeg'
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.before_request
def before_request():
   g.user = None
   if 'user' in session:
      g.user = Modelo.buscarU(session['user'])

@app.route("/")
def index():
  
   return render_template("./inicialekko.html")
   
   
@app.route('/B',methods= ['POST','GET'])
def B():
        f=request.files['archi']
        filename= secure_filename(f.filename)
        usuario=f.save(os.path.join(app.config['UPLOAD_FOLDER5'],filename))
        user=request.form['archi']
        if usuario == True:
           session['user'] = user 
           Modelo.entities(user, 'subir contrato', 'Se subio el contrato exitosamente')
           return redirect(url_for('logeado'))
        else:
            errorlog= "Te faltan campos"
            Modelo.entities(user, 'Error al subir contrato', 'No se pudo subir el contrato')
            return render_template('perfil.html', errorlog = errorlog) 

@app.route('/uploadContract',methods= ['POST','GET'])
def uploadContract():
        print("si llego")
        busqueda= Modelo.buscarU(session['user'])

        files = request.files.getlist('files[]')
	
        errors = {}
        success = False
      
        for file in files:
         if file:
            filename = secure_filename(file.filename)
            _nombrearchivo=filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER5'], filename))
            success = True

        if success:
            resp = json.jsonify({'message' : 'Files successfully uploaded'})
            _nombrearchivo=filename
            _urline="./static/Contratos\\"+filename
            resp.status_code = 201
            Modelo.entities(busqueda,'uploadContract','Subio contrato exitosamente')
            return resp

@app.route('/ID',methods= ['POST','GET'])
def ID():
        print("si llego")
        busqueda= Modelo.buscarU(session['user'])

        files = request.files.getlist('files[]')
	
        errors = {}
        success = False
      
        for file in files:
         if file:
            filename = secure_filename(file.filename)
            _nombrearchivo=filename
            Modelo.IngresarIDelante(busqueda,_nombrearchivo)            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True

        if success:
            resp = json.jsonify({'message' : 'Files successfully uploaded'})
            _nombrearchivo=filename
            _urline="./static/INEDELANTE\\"+filename
            Modelo.ImagenATextoINE(busqueda,_urline)
            #Modelo.IngresarIDelante(_nombrearchivo)
            resp.status_code = 201
            Modelo.entities(busqueda,'uploadINE','Subio su INE DELANTE')
            return resp
  
  
@app.route('/IDR',methods= ['POST','GET'])
def IDR():
    print("si llego")
    busqueda= Modelo.buscarU(session['user'])

    files = request.files.getlist('files[]')
	
    errors = {}
    success = False

    for file in files:
      if file:
         filename = secure_filename(file.filename)
         _nombrearchivo=filename
         Modelo.IngresarIDetras(busqueda,_nombrearchivo)
        
         file.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename))
         success = True

    if success:
       resp = json.jsonify({'message' : 'Files successfully uploaded'})
       _urline="./static/INEATRAS\\"+filename
       Modelo.ImagenATextoINEAtras(busqueda,_urline)
       resp.status_code = 201
       Modelo.entities(busqueda,'uploadINETR','Subio su INE DETRAS')
       return resp

       

@app.route('/COMP',methods= ['POST','GET'])
def COMP():
        print("si llego")
        busqueda= Modelo.buscarU(session['user'])

        files = request.files.getlist('files[]')
	
        errors = {}
        success = False
      
        for file in files:
         if file:
            filename = secure_filename(file.filename)
            _nombrearchivo=filename
            Modelo.IngresarComprobante(busqueda,_nombrearchivo)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER3'], filename))
            success = True

        if success:
            resp = json.jsonify({'message' : 'Files successfully uploaded'})
            _urline="./static/Comprobante\\"+filename
            Modelo.ImagenATextoDomicilio(busqueda,_urline)
            resp.status_code = 201
            Modelo.entities(busqueda,'uploadCompr','Subio su comprobante de domicilio')
            return resp

@app.route("/misdatos",methods=['GET', 'POST'] )

def misdatos():
   busqueda= Modelo.buscarU(session['user'])
   _name=Modelo.SelectNombre(busqueda)
   _rfc=Modelo.SelectCurp(busqueda)
   _email=busqueda
   _direccion=Modelo.SelectDireccion(busqueda)
   _fechanacimiento=Modelo.SelectFecha(busqueda)
   Modelo.CrearPDF(_name,_rfc,_email,_direccion,_fechanacimiento)
   Modelo.EnviarCorreoContrato(_name,_email)
   try:
      busquedaN= Modelo.SelectNombre(session['user'])
      busquedaEm= Modelo.SelectCorreo(session['user'])
      busquedaDI= Modelo.SelectDireccion(session['user'])
      busquedaFe= Modelo.SelectFecha(session['user'])
      busquedaCu= Modelo.SelectCurp(session['user'])

      return render_template("./datos.html",nombre=busquedaN,email=busquedaEm,direccion=busquedaDI,fechanaci=busquedaFe,curp=busquedaCu) 
   except:
      print("error")    

@app.route('/SELF',methods= ['POST','GET'])
def SELF():
        print("si llego")
        busqueda= Modelo.buscarU(session['user'])
        files = request.files.getlist('files[]')
	
        errors = {}
        success = False
      
        for file in files:
         if file:
            filename = secure_filename(file.filename)
            _nombrearchivo=filename
            Modelo.IngresarSelfie(busqueda,_nombrearchivo)
            file.save(os.path.join(app.config['UPLOAD_FOLDER4'], filename))
            success = True

        if success:
            resp = json.jsonify({'message' : 'Files successfully uploaded'})
            resp.status_code = 201            
            Modelo.entities(busqueda,'busqueda','Subio su selfie')
            return resp



@app.route("/registro",methods=['GET', 'POST'])
def insertarEventoP():
    if request.method == 'POST':
        _email=request.form.get('DEmail')
        _password=request.form.get('DPassword')
        usuario = Modelo.insertarEventoP(_email,_password)
        
        user=request.form['DEmail']
        if usuario == True:
           session['user'] = user 
           Modelo.entities(user, 'registrarse', 'El usuario se registro')
           Modelo.CorreoRegistro(_email)
           return redirect(url_for('index'))
        else:
            errorlog= "Te faltan campos"
            Modelo.entities(user, 'Error al registrarse', 'El usuario se registro')
            return render_template('registro.html', errorlog = errorlog)
     
               
    return render_template ("./registro.html")

              
@app.route("/actualizar")
def actualizarPass():
    if request.method == 'POST':
        _email=request.form.get('DEmailA')
        _password=request.form.get('DPasswordA')
        usuario=Modelo.actualizarM(_email,_password)
        user=request.form['DEmailA']
        if usuario == True:
           session['user'] = user 
           Modelo.entities(user, 'registrarse', 'El usuario se registro')
           #Modelo.EnviarCorreo(_name,_email)
           return redirect(url_for('index'))
        else:
            errorlog= "Te faltan campos"
            Modelo.entities(user, 'Error al registrarse', 'No pudo registrarse')
            return render_template('registro.html', errorlog = errorlog)

    return render_template("./actualizar.html")


@app.route("/login",methods=['GET', 'POST'])
def log():
   
   if g.user:
         return redirect(url_for('logea'))
   if request.method=='POST':
         session.pop('user', None)
         user=request.form['LEmail']
         password= request.form['LPassword']
         if (user and password):
            usuario= Modelo.validarUsuario(user,password)
            if usuario == True:
               session['user'] = user 
               Modelo.entities(user, 'Login', 'El usuario hizo log')
               return redirect(url_for('logea'))
            else:
               errorlog = "Tus datos son incorrectos"
               Modelo.entities(user, 'Login.Fail.NotFound', "Ingreso mal sus datos")
               return render_template('login.html',errorlog = errorlog)   
   return render_template('login.html')
 

@app.route("/logeado")
def logea():
  
  
   try:
      busqueda= Modelo.buscarU(session['user'])
      Modelo.entities(busqueda,'Perfil','El usuario entro a su perfil')
      return render_template("./perfil.html",usuarioactual=busqueda) 
   except:
      print("error")   

@app.route("/didocumentos",methods=['GET', 'POST'] )
def subdocumentos():
   busqueda= Modelo.buscarU(session['user'])
   Modelo.entities(busqueda,'documentos','Entro a mis documentos')
   return render_template("./documentos.html")   


@app.route("/actualizar")
def ActualizarEventoP():

   return render_template("./actualizar.html")

@app.route("/cerrar")
def cerrar():
   busqueda= Modelo.buscarU(session['user'])
   Modelo.entities(busqueda,'Logout','El usuario cerro sesión')
   session.pop("user",None)
   return redirect(url_for("index"))

        

if __name__ == "__main__":
    app.run()   
