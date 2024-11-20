#for FAST_AGINGGAN
1.  python3.8 -m venv myenv
2.  source myenv/bin/activate 
3.  pip install -r requirements.txt
4. pip install protobuf==3.20.0
5.  After virtual env is sucessfull created copy the folder myenv and place it inside ESRGAN also
6.  change ckpt path in infer.py to your relative path
7.  To run the the model : python infer.py --image_dir ./img
8.  resuls will be stored in your root directory if you are using streamlit
9.  if you are running the model manually then the results will be stored in the root directory for FAST_AGINGGAN
10.  result file name will be mygraph.png

#For ESR GAN
1. copy myenv from FAST_AGINGGAN
2. source myenv/bin/activate
3. pip install opencv-python
4. change the model path to your relative path in test.py
5. Download models from here : https://drive.google.com/drive/u/0/folders/17VYV_SoZZesU6mbxz2dMAIccSSlqLecY
6. to run the model : python test.py
7. results for both manual and streamlit will be stored in the ESRGAN/results folder


NOTE :
DO not enter the virtual enviroment when running app.py file in root directory streamlit will do this on his own