import random


panties = ["lace panties" , "floral pattern embroidery panties" , "satin panties" , "embroidery panties" , "floral pattern embroidery panties"]
panties_color = ["white panties" , "blue panties" , "pink panties"]
bras = ["bow bra, bow bra", "floral pattern embroidery bra" , "rose pattern embroidery bra"  , "satin bra"]
bra_color = ["white bra" , "blue bra" , "pink bra"]

dics : dict = {
    "[face]" : {"frown" , "smile" } ,
    "[crotch]" : {"nsfw , vaginal , pussy " , f"{random.choice(panties)} , {random.choice(panties_color)}"} , 
    "[foot]" : {"zettai ryouiki , thighhighs" , "bare foot"} , 
    "[sitting]" : {"on chair , in classroom" , "on bed, indoors"},
    "[missionaryFace]" : { "open eyes ,  open mouth,  one eye closed , cum in pussy  (trembling:1.4)" , "frown , clenched teeth , (motion lines:1.3)" } , 
    "[missionaryMove]" : { "sweat"  , "tearing up , one eye closed , (motion lines:1.5)" } , 
    "[missionaryHands]" : {"arms up" , "hands on own chest" , "breasts squeezed together"} , 
    "[panties]" : {f"{random.choice(panties)} , {random.choice(panties_color)}"} , 
    "[bras]" :  {f"{random.choice(bras)} , {random.choice(bra_color)}"} , 
    "[lingrie]" : {"shiny skin" ,  f"(nude:1.1),  {random.choice(bras)} , panties , detail bra , detail panties , focus bra , focus panties"}
}

lamys = {
    "alamy" : "<lora:lora_yukihana_lamy1:0.9:OUTD> , aalamy, long hair, streaked hair, ahoge, braid, beret, white headwear, hair flower, blue bowtie, cleavage, clothing cutout, white shirt, off shoulder, sleeveless, black corset, blue coat, snowflake print, fur-trimmed coat, open clothes, white thighhighs, brown belt, blue skirt", 
    "blamy" : "<lora:lora_yukihana_lamy1:0.9:OUTD> , bblamy, low twintails, streaked hair, ahoge, hairclip, japanese clothes, blue kimono, print kimono, blue hakama, floral print, long sleeves, sleeves past wrists, sash, hakama skirt" ,
    "clamy" : "<lora:lora_yukihana_lamy1:0.9:OUTD> , cclamy, ponytail, streaked hair, ahoge, hair flower, sailor collar, o-ring, sailor bikini, swimsuit, bikini skirt, pleated skirt, thigh strap",
    "dlamy1" : "<lora:lora_yukihana_lamy1:0.9:OUTD> , ddlamy, twintails, streaked hair, ahoge, hair ribbon, black ribbon, jewelry, plaid, frills, brown dress, white cardigan, open clothes, long sleeves, sleeves past wrists",
    "dlamy2" : "<lora:lora_yukihana_lamy1:0.9:OUTD> , ddlamy, twintails, streaked hair, ahoge, hair ribbon, black ribbon, jewelry, plaid, frills, brown dress, short sleeves" ,
    "elamy" : "<lora:lora_yukihana_lamy1:0.9:OUTD> , eelamy, short hair, streaked hair, ahoge, hair ornament, cleavage, polka dot, white camisole, white skirt, off shoulder, blue jacket, striped jacket, open clothes, long sleeves, sleeves past wrists, midriff"
}

lamysNude = {
    "alamy" : "<lora:lora_yukihana_lamy1:0.9:OUTD> , aalamy, long hair, streaked hair, ahoge, braid, beret, white headwear, hair flower, blue bowtie", 
    "blamy" : "<lora:lora_yukihana_lamy1:0.9:OUTD> , bblamy, low twintails, streaked hair, ahoge, hairclip, japanese clothes, " ,
    "clamy" : "<lora:lora_yukihana_lamy1:0.9:OUTD> , cclamy, ponytail, streaked hair, ahoge, hair flower",
    "dlamy1" : "<lora:lora_yukihana_lamy1:0.9:OUTD> , ddlamy, twintails, streaked hair, ahoge, hair ribbon, black ribbon, jewelry, plaid",
    "elamy" : "<lora:lora_yukihana_lamy1:0.9:OUTD> , eelamy, short hair, streaked hair, ahoge, hair ornament, cleavage"
}

suisei = {
    "sui1" : "<lora:hoshimachi_suisei_v1:1:1:lbw=OUTD> sui1, 1girl, solo, side ponytail, hoshimachi suisei, fingerless gloves, single thighhigh, jewelry, single sock, thigh strap, bracelet, blue socks, buttons, single kneehigh, plaid dress, blue choker, blue belt, plaid skirt, mini crown, grey skirt, blue ascot, long sleeves, plaid jacket ",
    "sui3" : "<lora:hoshimachi_suisei_v1:1:1:lbw=OUTD>  sui3, 1girl, solo, side ponytail, hoshimachi suisei, solo, white jacket, animal hood, white socks, open jacket, pleated skirt, black skirt, black sailor collar, black choker, school uniform, black shirt, puffy long sleeves } , { sweat | 2:: (torn clothes,  torn legwear,  torn shirt,  torn skirt:1.4) }"
}