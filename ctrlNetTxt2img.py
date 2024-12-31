from collections.abc import Iterable
import io
from typing import Any
import cv2
import base64
import requests
from PIL import Image
import datetime
import random
import webuiapi
import glob
import PromptDic


panties = ["lace panties" , "floral pattern embroidery panties" , "satin panties" , "embroidery panties" , "floral pattern embroidery panties"]
panties_color = ["white panties" , "blue panties" , "pink panties"]

class ctrlnetSetting:
    ModuleName = ""
    ModelName = ""
    Weight = 0.0
    def __init__(self , model , module , weight):
        self.ModuleName = module
        self.ModelName = model
        self.Weight = weight

class imgPrompt:
    Name = None
    BasePrompt = ""
    Prompt = ""
    ImgDir : str
    Ctrlnet : ctrlnetSetting
    Prompt = ""
    Step = 40
    Batch = 1
    RandomDic = {
        "[Face]" : ["smile" , "frown"]
    }
    
    def updatePrompt(self, p:str , d:list):
        for val in d:
            randomValues = list(d[val])
            p = p.replace( val ,  random.choice(randomValues))
        return p
    
    def Update(self):
        self.Prompt = self.updatePrompt(self.BasePrompt , self.RandomDic)
        return self.Prompt

    def __init__(self , name:str , dir:str , prompt:str ,  randomDic:list):
        self.Name = name
        self.ImgDir = dir
        self.BasePrompt = prompt
        self.RandomDic = randomDic
        self.Prompt = self.updatePrompt(p=prompt ,d=randomDic)

soleDic = {
    "[X]" : {"vaginal , pussy " , "panties"} , 
    "[Y]" : {"zettai ryouiki" , "bare foot"}
}

imgSole = imgPrompt(name="Sole" ,  dir ="C:\イラスト関係\成果\保存\Controlnet\足裏" , prompt=f"front(1.3) sitting , on chair , on chair , classroom, sole, focus face , skirt , [Y] , [X]" , randomDic=soleDic )
imgSole.Ctrlnet = [
    ctrlnetSetting(model="control_v11f1p_sd15_depth_fp16 [4b72d323]" ,  module="depth_midas" , weight=0.7)
]
missionary = imgPrompt(name="Sole" ,  dir ="C:\イラスト関係\成果\保存\Controlnet\足裏" , prompt=f"front(1.3) sitting , on chair , on chair , classroom, sole, focus face , skirt , [Y] , [X]" , randomDic=soleDic )


# A1111 URL
url = "http://127.0.0.1:7861"

# Read Image in RGB order

# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\11.png") # マルチフェラ
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\17.png") # 足広げ
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\18.png") # 横向き　四つん這い


# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\19.png") # 横からフェラ
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\20.png") # 後ろ　四つん這い
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\21.png") # 足広げ
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\28.png") # 自撮りピース　高難易度
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\32.png") # 足上げ
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\65.png") # 肌かくし
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\66.png") # 肌かくし 高難易度
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\67.png") # 肌かくし
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\68.png") # 肌かくし
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\71.png") # パイズリ
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\72.png") # パイズリ
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\73.png") # 足裏
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\74.png") # 足裏
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\75.png") # 足裏
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\78.png") # 足裏
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\81.png") # バック
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\82.png") # バック
# img = cv2.imread(r"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\83.png") # バック

# Encode into PNG and send to ControlNet
# retval, bytes = cv2.imencode('.png', img)
# encoded_image = base64.b64encode(bytes).decode('utf-8')

worst = "(worst quality, low quality:1.4), (EasyNegativeV2:1.1) , (bad_prompt_version2:1.1),(negative_hand-neg:1.4),(interlocked fingers:1.2), locked arms, animal ears, necktie, 4 legs, 3 legs, thighhighs, low quality, worst quality, out of focus, ugly, error, jpeg artifacts, lowers, blurry, bokeh, black bra, black panties, black lingerie,speech bubble, splatoon \(series\), splatoon 1, splatoon 1, bopoorly_drawn_hands,malformed_hands,missing_limb,floating_limbs,disconnected_limbs,extra_fingers,bad fingers,liquid fingers,poorly drawn fingers,missing fingers,extra digit,fewer digits,ugly open mouth,deformed eyes,partial open mouth,partial head,bad open mouth,inaccurate limb,cropped,too much muscle, black bra, black panties, black lingerie, (fused digit:1.3), (poorly drawn digit:1.3), (abnormal digit:1.3), (one hand with more than five digit:1.1), (too long digit:1.1), missing digit, (three legs:1.3), (poorly drawn legs:1.3), (fused legs:1.3), abnormal legs, missing legs, huge thighs, fused shoes,poorly drawn face, blurred background, background without depth, (fused hands:1.3), (poorly drawn hands:1.3), (abnormal hands:1.3), three hands, missing hands, low quality, worst quality, out of focus, ugly, error, jpeg artifacts, lowers, blurry, watermark,signature , multiple views, spoken , watermark, cotton bra , cotton panties , (noise:1.3), (deformed:1.3), (grayscale:1.3),(hands poor:1.2), (fingers poor:1.2), (bad anatomy:1.2), (inaccurate limb:1.2), (extra hands:1.2), (inaccurate limb:1.2),(deformed fingers:1.2), (extra fingers:1.2),(long body:1.2), (long neck:1.2), (long arm:1.2), (long leg:1.2), (extra arms:1.2), (extra legs:1.2), (extra navel:1.2),(ugly), (error), (poorly drawn), (missing), (mutation), (mutated), (liquid body), (bad proportions), (mosaic), (futa),(unnatural pose, color inconsistency,transparency issues,improper proportions, color scheme issues, image seams),(duplicate, morbid, mutilated,blurry, bad anatomy, disfigured,cropped, signature),bad face, fused face, poorly drawn face, cloned face, big face, long face, badeyes, fused eyes, poorly drawn eyes, extra eyes,dirty teeth, yellow teeth"
basePrompt =  "game cg,  shiny hair,  shiny skin,  (perfect anatomy:1.2) 1girl, solo BREAK"
# facial = ", cry , sad, streaming tears , tearing up , embarrassed , saliva, saliva trail, saliva drop , open mouth "
# facial = "{ open eyes ,  open mouth, smile , cum in pussy  ,( trembling:1.4) | frown , clenched teeth , tearing up , one eye closed , (motion lines:1.5),  } ,  looking at viewer,  sweat"
facial = "panic , open mouth , sweat , embarrassed"

costume = ""#", {(nude, naked:1.3) | sweat } , "
# facial = ", smile , embarrassed , "

blueArchiveChar = { 
# "serika" : "serikadef ,  (black hair ,  red eyes:1.3) , animal ear, twin tale",
# "hina" : "hinadef, silver hair ,  teen , purple eyes",
# "toki" : "tokidef, blonde hair , blue eyes",
# "hoshino" : "hoshinodef, pink hair , orange eyes",
# "miyakodef" : "miyakodef , silver hair , grey eyes",
# "hifumi" : "hifumidef, yellow eyes,  blonde hair",
# "mika" : "mikadef , pink hair , orange eyes" ,
# "shiroko" : "shirokodef, silver hair, blue eyes, animal ears, blue scarf" , 
"aris" : "arissailor , black hair, long hair",
# "yuuka" : "{yuukadef | yuukaidol | yuukagym } , black hair, blue eyes"
# "yuuka" : "yuukadef , black hair, blue eyes"
}

pantie_image = ["17","21","32"]
sole = ["73","74","75","78"]
#全般的に難しい
back = ["80", "81","82","83","84"]
cowgiral = ["59" , "60", "61" , "62"]

cnt = 0
today = str(datetime.datetime.today().date())

##


files = glob.glob(f"{imgSole.ImgDir}\*.png")
hires = 1

for num in range(2) :
    # img = Image.open(file)
    # prompt = imgSole.Update()
    api = webuiapi.WebUIApi(host="127.0.0.1" , port=7860 , sampler="DPM++ 3M SDE Exponential" , steps=80)

    samplers = api.get_samplers()
    scripts = api.get_scripts()

    r = api.txt2img(
        enable_hr = True if hires == 1 else False,
        denoising_strength=0.45,
        hr_scale=2,
        # controlnet_units=controlnet_units,
        hr_upscaler="R-ESRGAN 4x+ Anime6B",
        cfg_scale=7,
        width=512,
        height=768,
        prompt=imgSole.Update(),
        negative_prompt= worst,
        batch_size=1,
        hr_second_pass_steps=20,
        alwayson_scripts={"dynamic prompts v2.16.3":[]} # wildcards extension doesn't accept more parameters.
    )
    
    images = r.images[:-2 if hires == 1 else -1]
    for image in images:
        today = datetime.datetime.today().strftime("%Y_%m_%d_%H%M%S")
        output_path = today + "_" +  str(cnt).zfill(3) +'.png'
        image.save(output_path)
        print(output_path)
        cnt += 1

## contorlnet 用
# for file in files:
#     img = Image.open(file)
#     prompt = imgSole.Update()
#     api = webuiapi.WebUIApi(host="127.0.0.1" , port=7860 , sampler="DPM++ 3M SDE Exponential" , steps=80)

#     samplers = api.get_samplers()
#     scripts = api.get_scripts()

#     controlnet_units = []
#     ctrl = imgSole.Ctrlnet[0]
#     unit1 = webuiapi.ControlNetUnit(input_image=img, model=ctrl.ModelName , module=ctrl.ModuleName , weight=0.5 , control_mode = 1 )
#     controlnet_units.append(unit1)
#     r = api.txt2img(
#         enable_hr = True if hires == 1 else False,
#         denoising_strength=0.45,
#         hr_scale=2,
#         controlnet_units=controlnet_units,
#         hr_upscaler="R-ESRGAN 4x+ Anime6B",
#         cfg_scale=7,
#         width=512,
#         height=768,
#         prompt=imgSole.Update(),
#         negative_prompt= worst,
#         batch_size=1,
#         hr_second_pass_steps=20,
#         # alwayson_scripts={"dynamic prompts v2.16.1":[]} # wildcards extension doesn't accept more parameters.
#     )
    
#     images = r.images[:-2 if hires == 1 else -1]
#     for image in images:
#         today = datetime.datetime.today().strftime("%Y_%m_%d_%H%M%S")
#         output_path = today + "_" +  str(cnt).zfill(3) +'.png'
#         image.save(output_path)
#         print(output_path)
#         cnt += 1
##

for num in range(1):
    path = rf"C:\Users\Sample\Downloads\DepthNSFWAnimePoses_v40\Depth\{random.choice(sole)}.png"
    img = Image.open(path)
    print(path)
    charaIndex = random.randrange(len(PromptDic.suisei))
    chars = list(blueArchiveChar.keys())
    charaPrompt = blueArchiveChar[chars[charaIndex]]

    print("chara:" + chars[charaIndex])

    #ブルアカキャラ全般
    # charactor =  f"<lora:bluearchivefull1:0.9:OUTD> {charaPrompt} , {facial} , (nude:1.3) , vaginal , BREAK"
    charactor =  f"<lora:bluearchivefull1:0.9:OUTD> {charaPrompt} , {facial} , BREAK"
   
    # charactor =  "<lora:akane:1:OUTD> , Akane, white shirt, blue necktie, skirt, multicolored hair , bob cut , (nude:1.3) , " + facial + "BREAK"


    # 18
    # prompt = basePrompt + charactor +  "out doors , (sheets grab:1.3) , 1girl , (detail eyes , focus eyes:1.3) , <lora:bluearchivefull1:0.8:OUTD> {hinadef, silver hair , teen , purple eyes | tokidef, blonde hair , blue eyes } 1boy , all fours , doggy style , from behind, vaginal , looking at viewer ,  open mouth, {smile | cry ,sad , tearing up , streaming tears } , sweat, (nude:1.3) , narrow waist"

    # 19
    # prompt = basePrompt + charactor + "boy is standing , indoors , in classroom ,  ,  1boy , standing , (testicle , penis:1.3) , 1girl , tearing up ,  (detail eyes , focus eyes:1.3) , from side , licking penis , (fellatio:1.3) , facial , hetero "

    # 20
    # prompt = basePrompt + charactor + "indoors , on bed , embarrassed , (sheets grab:1.5) , looking at viewer, 1girl , (detail eyes , focus eyes:1.3) , <lora:bluearchivefull1:0.8:OUTD>  tokidef, blonde hair , blue eyes , all fours , doggy style , from behind, vaginal , sweat, (nude:1.3) , narrow waist"

    # 21
    # prompt = basePrompt + " , 1girl, 2boys, blush, hands on floor , breasts, bukkake, collarbone, cum, cum_in_mouth, cum_on_hair, ejaculation, facial, hetero, interracial, hands on floor , looking_at_viewer, multiple_penises, navel, open_mouth, penis, multiple penis , veny penis, projectile_cum, sitting, testicles , wariza" + charactor

    # 28
    # prompt = basePrompt + charactor + "smartphone , standing ,  v , BREAK"

    # 32 , 21 , 17　膝立　おすすめ
    # prompt = basePrompt + charactor + f", sitting , focus panties , detail panteis , <lora:flat2:-0.1> , {{vaginal , pussy | {random.choice(panties)} , {random.choice(panties_color)}}} BREAK"
    # prompt = basePrompt + charactor + f", sitting , focus panties , detail panteis , {random.choice(panties)} , {random.choice(panties_color)}  BREAK"

    # 59~62
    # prompt = basePrompt + charactor + " 1boy , spread legs , on bed ,  cowgirl position , sex:1.2 , missionary , depth of field , indoors , hotel , hetero " #(nude:1.3) "


    #64～68　胸隠し
    # prompt = basePrompt + charactor + "hand on crotch  black hair, blue eyes" + facial + "BREAK"

    #72
    # prompt = basePrompt + charactor + "1boy , penis , paizuri ,  penis , breasts blowjob , breast squeeze , (cum on body , cum on breasts ,  facial , cum in penis , ejaculation, cum shot:1.3)"

    # 73 , 74 , 75, 76 , 77 足裏
    # prompt = basePrompt + charactor + f"(front:1.3)   sitting , on chair , front , on chair , classroom, sole, focus face , skirt , {{ bare foot | black zettai ryouiki }} , {random.choice(panties)} , {random.choice(panties_color)} , <lora:flat2:-0.2>" #, (panties under pantyhose:1.3),
    
    pantie = random.choice(panties)
    # prompt = basePrompt + charactor + f"(front:1.3) , sitting , {{ on chair , classroom | on bed, indoors }}, sole, focus face , black zettai ryouiki , {{pussy , vaginal | {{{random.choice(panties)}}} , {{{random.choice(panties_color)}}} }}"
    prompt = basePrompt + charactor + f"(front:1.2) , sitting , on chair , in classroom , focus face , skirt , {random.choice(panties)} , {random.choice(panties_color)}"
    print(prompt)
    #80 , 81,82,83,84
    # prompt = basePrompt + charactor + " (1boy , hide boy face, missionary , torso grab , doggystyle , standing , sex:1.2) , depth of field , indoors , hotel , hetero" #(nude:1.3) "

    hires = 1
    batch = 1
    # create API client with custom host, port
    api = webuiapi.WebUIApi(host="127.0.0.1" , port=7860 , sampler="DPM++ 2M SDE Karras" , steps=40)
    controlnet_units = []
    unit1 = webuiapi.ControlNetUnit(input_image=img, model='control_v11f1p_sd15_depth_fp16 [4b72d323]' , weight=0.5 , control_mode = 1 )
    controlnet_units.append(unit1)
    r = api.txt2img(
        enable_hr = True if hires == 1 else False  ,
        denoising_strength=0.55,
        hr_scale=2,
        controlnet_units=controlnet_units,
        hr_upscaler="R-ESRGAN 4x+ Anime6B",
        cfg_scale=7,
        width=512,
        height=768,
        prompt=prompt,
        negative_prompt= worst,
        batch_size=batch,
        hr_second_pass_steps=20
        # alwayson_scripts={"dynamic prompts v2.16.1":[]} # wildcards extension doesn't accept more parameters.
    )
    print(num)

    images = r.images[:-2 if hires == 1 else -1]
    for image in images:
        today = datetime.datetime.today().strftime("%Y_%m_%d_%H%M%S")
        output_path = today + "_" +  str(cnt).zfill(3) +'.png'
        image.save(output_path)
        print(output_path)
        cnt += 1
