# Voice-Stable-Diffusion

This repository contains the implementation of a Voice-assited Streamlit application to generate Images With Stable Diffusion. You can read the blog on Medium here: [Medium Blog](https://medium.com/@avi_chawla/66b7facd8fc4). 

Befor running the application, you should:

1. Get the AssemblyAI API Key from [here](https://app.assemblyai.com/). In `app.py`, define the API key as `assembly_auth_key`(line 15).
2. Get the Stable Diffusion API Key from [here](https://replicate.com/). In terminal, execute the following command: 

`export REPLICATE_API_TOKEN=Your-auth-key`

Other requirements are listed in requirements.txt file.

To run the application, run the following command in terminal:

    streamlit run app.py

The above command should open a browser where you can use the application.  

![image](https://user-images.githubusercontent.com/36801774/197845024-07a2c393-be50-436e-a36e-acc1e36653f2.png)
