# anime_video_converter
- Install dependences
  
` pip install -r requirements.txt` 

- Migrate

` python manage.py migrate `

- Run server

` python manage.py runserver `

- Run Model AI

` python video2anime.py  --video video/input/demo.mp4  --checkpoint_dir  ./checkpoint/generator_Hayao_weight  `