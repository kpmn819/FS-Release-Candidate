# Data Module2

# _________ START DEFINE DICTIONARIES ______________
# key dictionary first the modifiers
mod_dict = {
    'nul':0,
    'shf':2, #was 32 
    'ctl':1,# was 16
    'alt':4, # was 64
    'ctlshf':3,
    'altshf':6,
    'altctl':5
}
# now the letter and other physical keys
key_dict = {
    'nul':0,
    'a':4,
    'b':5,
    'c':6,
    'r':21,
    't':23,
    'z':29,
    'o':18,
    's':22,
    'n':17,
    'y':28,
    'g':10,
    'f':9,
    'd':7,
    'x':27,
    'u':24,
    'v':25,
    'w':26,
    'pg_dn':78,
    'pg_up':75,
    'end_key':77,
    'delete':76,
    'insert':73,
    'home':74,
    '[':47,
    ']':48,
    '|':49,
    'F6':63,
    'F7':64,
    'num_1':89,
    'num_7':95,
    'num_del':99
}

# 
# layout {'name'[0],x1[1],x2[2],y1[3],y2[4],key_mod[5],key_code[6],status[7], number[8]}
# status can be 'off' 'on' for latching buttons, number is the number of times the key is pressed
# 
# first define the individual lists
# =['', ,,,, mod_dict[],key_dict[], '',1]

# page change the current page is not included in the big list
ap_page =['ap_page.png', 870,975,230,260, mod_dict['nul'],key_dict['nul'], 'page', 1]
navcom_page =['navcom_page.png', 870,975,290,330, mod_dict['nul'],key_dict['nul'], 'page',1]
aux1_page =['aux1_page.png', 870,975,350,390, mod_dict['nul'],key_dict['nul'], 'page',1]
aux2_page =['aux2_page.png', 870,975,415,450, mod_dict['nul'],key_dict['nul'], 'page',1]

# Autopilot
dec_ref_alt =['dec_ref_alt', 675,785,510,540, mod_dict['ctl'],key_dict['pg_dn'], '', 1]
dec_ref_alt10  =['dec_ref_alt10', 505,605,510,540, mod_dict['ctl'],key_dict['pg_dn'], '', 5]
inc_ref_alt =['inc_ref_alt', 670,780,450,490, mod_dict['ctl'],key_dict['pg_up'], '', 1]
inc_ref_alt10  =['inc_ref_alt10', 500,610,450,480, mod_dict['ctl'],key_dict['pg_up'], '', 5]
tog_appr_hold =['tog_approach_hold', 100,250,325,375, mod_dict['ctl'],key_dict['a'], 'off', 1, 'green']
#tog_alt_hold =['tog_altitude_hold', 100,250,125,175, mod_dict['ctl'],key_dict['t'], 'off', 1]
tog_apn1_hold =['ap_n1_hold', 100,250,225,275, mod_dict['ctl'],key_dict['n'], 'off', 1, 'green']
# ap_off =['ap_off', 300,450,25,75, mod_dict['altshf'],key_dict['z'], 'off', 1]
# need to reassign ap_on to ap master key binding alt ]
ap_on =['ap_on', 100,250,25,75, mod_dict['nul'],key_dict['z'], 'off', 1, 'red']
tog_fd =['tog_flight_dir', 500,660,325,385, mod_dict['ctl'],key_dict['f'], 'off', 1, 'blue']
tog_ap_alt_hold =['tog_ap_altitude', 100,250,125,175, mod_dict['nul'],key_dict['['], 'off', 1, 'blue']
tog_ap_flc =['tog_ap_flc', 100,250,525,575, mod_dict['ctl'],key_dict['['], 'off', 1, 'white']
tog_ap_hdg =['tog_ap_heading', 300,450,125,175, mod_dict['alt'],key_dict['['], 'off', 1, 'blue']

ap_hdg_left =['ap hdg left', 500,610,170,210, mod_dict['ctl'],key_dict['delete'], '',1]
ap_hdg_left_fast =['ap hdg left fast', 500,610,110,150, mod_dict['ctl'],key_dict['delete'], '',8]
ap_hdg_right =['ap hdg right', 670,785,170,210, mod_dict['ctl'],key_dict['insert'], '',1]
ap_hdg_right_fast =['ap hdg right fast', 670,775,110,210, mod_dict['ctl'],key_dict['insert'], '',8]


tog_ap_bc =['tog_ap_backcourse.png', 300,450,325,375, mod_dict['shf'],key_dict['['], 'off', 1, 'red']
tog_ap_vs =['tog_ap_vert_speed.png', 100,250,425,475, mod_dict['altshf'],key_dict['['], 'off', 1, 'white']

vs_up =['vs up', 210,375,410,450, mod_dict['ctl'],key_dict['home'], '',1]
vs_dn =['vs dn', 380,480,460,500, mod_dict['ctl'],key_dict['end_key'], '',1]
flc_up =['flc up', 275,380,500,550, mod_dict['ctlshf'],key_dict['insert'], '',1]
flc_dn =['flc dn', 375,480,550,590, mod_dict['ctlshf'],key_dict['delete'], '',1]

# radio entries are next

nav_freq_swap =['nav_freq_swap.png', 125,280,225,280, mod_dict['ctlshf'],key_dict['n'], '',1]
nav_rad_1_2 =['nav 1/2 swap', 150,250,335,375, mod_dict['nul'],key_dict['nul'], '',1]
inc_nav_frac =['inc_nav_frac.png', 215,325,400,450, mod_dict['ctlshf'],key_dict['pg_up'], '',1]
inc_nav_whole =['inc_nav_whole.png', 80,190,400,450, mod_dict['altshf'],key_dict['pg_up'], '',1]
dec_nav_whole =['dec_nav_whole.png', 80,190,500,540, mod_dict['altshf'],key_dict['pg_dn'], '',1]
dec_nav_frac =['dec_nav_frac.png', 225,325,500,540, mod_dict['ctlshf'],key_dict['pg_dn'], '',1]

com_freq_swap =['com_freq_swap.png', 470,630,220,280, mod_dict['nul'],key_dict[']'], '',1]
com_rad_1_2 =['com 1/2 swap', 490,600,330,370, mod_dict['nul'],key_dict['nul'], '',1]
inc_com_frac =['inc_com_frac.png', 570,680,400,450, mod_dict['altctl'],key_dict[']'], '',1]
inc_com_whole =['inc_com_whole.png', 410,520,400,450, mod_dict['ctlshf'],key_dict[']'], '',1]
dec_com_frac =['dec_com_frac.png', 570,675,500,535, mod_dict['ctl'],key_dict[']'], '',1]
dec_com_whole =['dec_com_whole.png', 410,520,500,535, mod_dict['shf'],key_dict[']'], '',1]

# now some aux1 entries
flaps_up =['flaps up', 100,260,135,200, mod_dict['nul'],key_dict['F6'], 'multi',1]
flaps_dn =['flaps dn', 100,260,270,330, mod_dict['shf'],key_dict['F6'], 'multi',1, '']
trim_up =['trim up', 330,500,135,200, mod_dict['nul'],key_dict['num_1'], '',1]
trim_dn =['flaps dn', 330,500,230,330, mod_dict['nul'],key_dict['num_7'], '',1]
park_brake =['park brake', 560,725,135,200, mod_dict['ctl'],key_dict['num_del'], 'on', 1, 'red']
# then add all the individual to the big_list
# this will allow us to iterate through all the entries to find a match
ap_list = [
    dec_ref_alt, dec_ref_alt10, inc_ref_alt, inc_ref_alt10, tog_appr_hold, 
    tog_apn1_hold, ap_on, tog_fd, tog_ap_alt_hold, tog_ap_flc, tog_ap_hdg,
    ap_hdg_left, ap_hdg_left_fast, ap_hdg_right, ap_hdg_right_fast, 
    tog_ap_bc, tog_ap_vs, navcom_page, aux1_page, aux2_page, vs_up, vs_dn,
    flc_up, flc_dn]

radio_list = [
    nav_freq_swap, inc_nav_frac, inc_nav_whole, dec_nav_frac, dec_nav_whole,
    com_freq_swap, inc_com_frac, inc_com_whole, dec_com_frac, dec_com_whole, ap_page, aux1_page, aux2_page]

aux1_list = [ap_page, navcom_page, aux2_page, flaps_up, flaps_dn, trim_up, trim_dn, park_brake]

aux2_list = [ap_page, navcom_page, aux1_page]
  
# _____________ END DEFINE DICTIONARIES _______________________


