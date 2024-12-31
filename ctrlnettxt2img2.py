from collections.abc import Iterable
import io
from typing import Any
from PIL import Image
import datetime
import random
import webuiapi
import glob
import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from collections import defaultdict
import PromptDic

base =  "game cg,  shiny hair,  shiny skin,  (perfect anatomy:1.2) 1girl, solo BREAK"
negative = "(worst quality, low quality:1.4), (EasyNegativeV2:1.1) , (bad_prompt_version2:1.1),(negative_hand-neg:1.4),(interlocked fingers:1.2), locked arms, animal ears, necktie, 4 legs, 3 legs, thighhighs, low quality, worst quality, out of focus, ugly, error, jpeg artifacts, lowers, blurry, bokeh, black bra, black panties, black lingerie,speech bubble, splatoon \(series\), splatoon 1, splatoon 1, bopoorly_drawn_hands,malformed_hands,missing_limb,floating_limbs,disconnected_limbs,extra_fingers,bad fingers,liquid fingers,poorly drawn fingers,missing fingers,extra digit,fewer digits,ugly open mouth,deformed eyes,partial open mouth,partial head,bad open mouth,inaccurate limb,cropped,too much muscle, black bra, black panties, black lingerie, (fused digit:1.3), (poorly drawn digit:1.3), (abnormal digit:1.3), (one hand with more than five digit:1.1), (too long digit:1.1), missing digit, (three legs:1.3), (poorly drawn legs:1.3), (fused legs:1.3), abnormal legs, missing legs, huge thighs, fused shoes,poorly drawn face, blurred background, background without depth, (fused hands:1.3), (poorly drawn hands:1.3), (abnormal hands:1.3), three hands, missing hands, low quality, worst quality, out of focus, ugly, error, jpeg artifacts, lowers, blurry, watermark,signature , multiple views, spoken , watermark, cotton bra , cotton panties , (noise:1.3), (deformed:1.3), (grayscale:1.3),(hands poor:1.2), (fingers poor:1.2), (bad anatomy:1.2), (inaccurate limb:1.2), (extra hands:1.2), (inaccurate limb:1.2),(deformed fingers:1.2), (extra fingers:1.2),(long body:1.2), (long neck:1.2), (long arm:1.2), (long leg:1.2), (extra arms:1.2), (extra legs:1.2), (extra navel:1.2),(ugly), (error), (poorly drawn), (missing), (mutation), (mutated), (liquid body), (bad proportions), (mosaic), (futa),(unnatural pose, color inconsistency,transparency issues,improper proportions, color scheme issues, image seams),(duplicate, morbid, mutilated,blurry, bad anatomy, disfigured,cropped, signature),bad face, fused face, poorly drawn face, cloned face, big face, long face, badeyes, fused eyes, poorly drawn eyes, extra eyes,dirty teeth, yellow teeth"


@dataclass_json
@dataclass
class CtrlnetSetting:
    ModuleName :str = ""
    ModelName :str = ""
    Weight :float = 0.0
    def __init__(self , model , module , weight):
        self.ModuleName = module
        self.ModelName = model
        self.Weight = weight


@dataclass_json
@dataclass
class imgPrompt:
    # Ctrlnet : ctrlnetSetting = ctrlnetSetting("","",0)
    
    def updatePrompt(self, p:str , d:list):
        for val in d:
            randomValues = list(d[val])
            p = p.replace( val ,  random.choice(randomValues))
        return p
    
    def UpdatePrompt(self:str):
        self.Prompt = self.updatePrompt(self.OriginalPrompt , PromptDic.dics)
        return self.Prompt
    
    def GetPrompt(self ,  char:str):
        return f"{self.BasePrompt} BREAK {char} BREAK {self.Prompt}"

    def GetPrompt(self ,  chars:dict):
        charaIndex = random.randrange(len(chars))
        charList = list(chars.keys())
        char = f"{chars[charList[charaIndex]]}"
        return f"{self.BasePrompt} BREAK {char} BREAK {self.Prompt}"


    def __init__(self , name:str = "", imgDir:str ="", prompt:str ="", step:int = 40, basePrompt:str = "" , originalPrompt="", negativePrompt = "" , batch:int = "" , width:int = 512 , height:int = 768 , strength:int = 0.7 , ctrlnetSetting:CtrlnetSetting = ("","", 0) , charas = {}):
        self.Name = name
        self.ImgDir = imgDir
        self.Prompt = prompt
        self.BasePrompt = basePrompt
        self.NegativePrompt = negativePrompt
        self.Ctrl = ctrlnetSetting
        self.Height = height
        self.Width = width
        self.Batch = batch
        self.Step = step
        self.Strength = strength
        self.Prompt = ""
        self.OriginalPrompt = originalPrompt
        self.Charas = charas
        self.UpdatePrompt()

imgSole = imgPrompt(
    name="Sole" ,  
    imgDir= "C:\イラスト関係\成果\保存\Controlnet\足裏" , 
    basePrompt=base,
    negativePrompt=negative,
    batch=1,
    strength=0.8,
    ctrlnetSetting = CtrlnetSetting(model="control_v11f1p_sd15_depth_fp16 [4b72d323]" ,  module="depth_midas" , weight=0.7),
    originalPrompt=f"smile , detail eyes,  open mouth , sweat , embarrassed , front(1.3) sitting , [sitting], focus face , skirt , [foot] , [panties]")

imgStandBra = imgPrompt(
    name="imgStandBra" ,  
    imgDir= "C:\イラスト関係\成果\保存\Controlnet\立ちブラ" , 
    basePrompt=base,
    negativePrompt=negative,
    batch=1,
    strength=0.45,
    ctrlnetSetting = CtrlnetSetting(model="control_v11f1p_sd15_depth_fp16 [4b72d323]" ,  module="depth_midas" , weight=0.7),
    originalPrompt=f"smile , indoors , hotel ,  sweat , embarrassed , front(1.3) , standing , focus bra , detail eyes , [bras] , panties")


# imgMissionary = imgPrompt(
#     name="Missionary" ,  
#     imgDir= "C:\イラスト関係\成果\保存\Controlnet\正常位" , 
#     basePrompt=base,
#     negativePrompt=negative,
#     step=120,
#     batch=1,
#     strength=0.45,
#     ctrlnetSetting = CtrlnetSetting(model="control_v11p_sd15_openpose_fp16 [73c2b67d]" ,  module="dw_openpose_full" , weight=0.45),
#     originalPrompt=f"straddling , cowgirl position, from below,  ceiling,  [missionaryFace] , [missionaryHands] , [missionaryMove] , 1boy , torso grab ,  vaginal, pov , (1boy, penis:1.3), spread legs , nose blush,  pussy juice"
# )


# imgCowgirl = imgPrompt(
#     name="Cowgirl" ,  
#     imgDir= "C:\イラスト関係\成果\保存\Controlnet\騎乗位" , 
#     basePrompt=base,
#     negativePrompt=negative,
#     step=120,
#     batch=1,
#     strength=0.45,
#     ctrlnetSetting = CtrlnetSetting(model="control_v11p_sd15_openpose_fp16 [73c2b67d]" ,  module="dw_openpose_full" , weight=0.45),
#     originalPrompt=f"straddling , on bed , cowgirl position, from below,  ceiling ,  [missionaryFace] , [missionaryHands] , [missionaryMove] , 1boy , torso grab ,  vaginal, pov , (1boy, penis:1.3), spread legs , nose blush,  pussy juice"
# )

#__nsp/my/new_panties__ ,  lace panties , focus panties , detail panties ,  ( knees together , legs closed:1.3) , (front:1.2),  hugging own legs  , smile , laughing , on floor , in doors 
# imgOther = imgPrompt(
#     name="Other" ,  
#     imgDir= "C:\イラスト関係\成果\保存\Controlnet\その他" , 
#     basePrompt=base,
#     negativePrompt=negative,
#     step=40,
#     batch=1,
#     strength=0.45,
#     ctrlnetSetting = CtrlnetSetting(model="control_v11p_sd15_openpose_fp16 [73c2b67d]" ,  module="dw_openpose_full" , weight=0.67),
#     originalPrompt=f" indoors , smile , embarrassed , [lingrie] "
# )

#パンツたくし上げ
imgPanties = imgPrompt(
    name="Panties" ,  
    imgDir= "C:\イラスト関係\成果\保存\Controlnet\パンツたくし上げ" , 
    basePrompt=base,
    negativePrompt=negative,
    step=60,
    batch=1,
    strength=0.6,
    ctrlnetSetting = CtrlnetSetting(model="control_v11p_sd15_openpose_fp16 [73c2b67d]" ,  module="dw_openpose_full" , weight=0.67),
    originalPrompt="nose blush, frown , embarrassed , lying , front ,spread legs,  ass , ([panties]:1.3)  , lifted by self, skirt lift, on bed , bottomless,  from below  , (focus crotch:1.5) , narrow waist, upper body")

# imgs = {imgSole , imgMissionary , imgCowgirl}

# with open("output_jp.json", "w", encoding="shift-jis") as outputFile:
#     outputFile.write(data)
# with open("output_jp.json", "r", encoding="shift-jis") as outputFile:
#     val = outputFile.read()
#     imgSole = imgPrompt.from_json(val)


# A1111 URL
url = "http://127.0.0.1:7860"

blueArchiveChar = { 
"serika" : "serikadef ,  (black hair ,  red eyes:1.3) , animal ear, twin tale",
# "hina" : "hinadef, silver hair ,  teen , purple eyes",
# "toki" : "tokidef, blonde hair , blue eyes",
# "hoshino" : "hoshinodef, pink hair , orange eyes",
# "miyakodef" : "miyakodef , silver hair , grey eyes",
# "hifumi" : "hifumidef, yellow eyes,  blonde hair",
# "mika" : "mikadef , pink hair , orange eyes" ,
# "shiroko" : "shirokodef, silver hair, blue eyes, animal ears, blue scarf" , 
# "aris" : "arissailor , black hair, long hair",
# "aris" : "arisdef , black hair, long hair , small breastes",
# "yuuka" : "{yuukadef | yuukaidol | yuukagym } , black hair, blue eyes",
}

# lamys = {
#     "alamy" : "<lora:lora_yukihana_lamy1:0.8:OUTD> , aalamy, long hair, streaked hair, ahoge, braid, beret, white headwear, hair flower, blue bowtie, cleavage, clothing cutout, white shirt, off shoulder, sleeveless, black corset, blue coat, snowflake print, fur-trimmed coat, open clothes, white thighhighs, brown belt, blue skirt", 
#     "blamy" : "<lora:lora_yukihana_lamy1:0.8:OUTD> , bblamy, low twintails, streaked hair, ahoge, hairclip, japanese clothes, blue kimono, print kimono, blue hakama, floral print, long sleeves, sleeves past wrists, sash, hakama skirt" ,
#     "clamy" : "<lora:lora_yukihana_lamy1:0.8:OUTD> , cclamy, ponytail, streaked hair, ahoge, hair flower, sailor collar, o-ring, sailor bikini, swimsuit, bikini skirt, pleated skirt, thigh strap",
#     "dlamy1" : "<lora:lora_yukihana_lamy1:0.8:OUTD> , ddlamy, twintails, streaked hair, ahoge, hair ribbon, black ribbon, jewelry, plaid, frills, brown dress, white cardigan, open clothes, long sleeves, sleeves past wrists",
#     "dlamy2" : "<lora:lora_yukihana_lamy1:0.8:OUTD> , ddlamy, twintails, streaked hair, ahoge, hair ribbon, black ribbon, jewelry, plaid, frills, brown dress, short sleeves" ,
#     "elamy" : "<lora:lora_yukihana_lamy1:0.8:OUTD> , eelamy, short hair, streaked hair, ahoge, hair ornament, cleavage, polka dot, white camisole, white skirt, off shoulder, blue jacket, striped jacket, open clothes, long sleeves, sleeves past wrists, midriff"
# }

cnt = 0
today = str(datetime.datetime.today().date())

##

# charaIndex = random.randrange(len(blueArchiveChar))
# chars = list(blueArchiveChar.keys())
# charaPrompt = blueArchiveChar[chars[charaIndex]]
# print("chara:" + chars[charaIndex])


# charaIndex = random.randrange(len(lamys))
# chars = list(lamys.keys())
# charaPrompt = f"<lora:lora_yukihana_lamy1:0.8:OUTD> {lamys[chars[charaIndex]]}"
# print("chara:" + chars[charaIndex])




# charactor =  f"<lora:bluearchivefull1:1:OUTD> {charaPrompt} BREAK"
# charactor = f"{charaPrompt}"

current : imgPrompt = imgSole


files = glob.glob(f"{current.ImgDir}\*.png")#[:2]
# for n in range(2):
#     for file in files:
#         img = Image.open(file)
#         api = webuiapi.WebUIApi(host="127.0.0.1" , port=7860 , sampler="DPM++ 2M SDE Karras" , steps=current.Step)
#         controlnet_units = []
#         ctrl : CtrlnetSetting = current.Ctrl#.CtrlnetSetting#[0]
#         unit1 = webuiapi.ControlNetUnit(input_image=img, model=ctrl.ModelName , module=ctrl.ModuleName , weight=ctrl.Weight, control_mode = 1 )
#         controlnet_units.append(unit1)
#         current.UpdatePrompt()
#         prompt = current.GetPrompt(PromptDic.lamysNude),
#         print(prompt)
#         # print(current.Prompt)
#         r = api.txt2img(
#             enable_hr = True if hires == 1 else False,
#             denoising_strength=current.Strength,
#             hr_scale=2,
#             controlnet_units=controlnet_units,
#             hr_upscaler="R-ESRGAN 4x+ Anime6B",
#             cfg_scale=7,
#             width=current.Width,
#             height=current.Height,
#             prompt=  str(prompt) ,
#             negative_prompt= current.NegativePrompt,
#             batch_size=current.Batch,
#             hr_second_pass_steps=20,
#             alwayson_scripts={"dynamic prompts v2.16.1":[]}
#         )
#         images = r.images[:-2 if hires == 1 else -1]
#         for image in images:
#             today = datetime.datetime.today().strftime("%Y_%m_%d_%H%M%S")
#             output_path = today + "_" +  str(cnt).zfill(3) +'.png'
#             image.save(output_path)
#             print(output_path)

#             cnt += 1
##


hires = 0

for n in range(1):
    # img = Image.open(file)
    api = webuiapi.WebUIApi(host="127.0.0.1" , port=7860 , sampler="DPM++ 3M SDE Exponential" , steps=80)
    # controlnet_units = []
    # ctrl : CtrlnetSetting = current.Ctrl
    # unit1 = webuiapi.ControlNetUnit(input_image=img, model=ctrl.ModelName , module=ctrl.ModuleName , weight=ctrl.Weight, control_mode = 1 )
    # controlnet_units.append(unit1)
    # current.UpdatePrompt()
    # prompt = current.GetPrompt(PromptDic.lamysNude),
    # print(prompt)
    # print(current.Prompt)
    r = api.txt2img(
        enable_hr = True if hires == 1 else False,
        denoising_strength=current.Strength,
        hr_scale=2,
        # controlnet_units=controlnet_units,
        hr_upscaler="R-ESRGAN 4x+ Anime6B",
        cfg_scale=7,
        width=current.Width,
        height=current.Height,
        prompt= "1girl , solo , school uniform , wariza , on bed , arms on bed , { black hair | blonde hair } ",
        negative_prompt= current.NegativePrompt,
        batch_size=3,
        save_images=True,
        hr_second_pass_steps=20,
        alwayson_scripts={"dynamic prompts v2.16.3":[]}
    )

    print(r.info["all_prompts"])
    images = r.images
    for image in images:
        today = datetime.datetime.today().strftime("%Y_%m_%d_%H%M%S")
        output_path = today + "_" +  str(cnt).zfill(3) +'.png'
        print(image.info)
        image.save(output_path)
        print(output_path)

        cnt += 1
##