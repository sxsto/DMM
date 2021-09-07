import socket
import base64
import http.client
import json
import os
import sys
import logging
import time
import urllib.parse
logging.basicConfig(level=logging.INFO,format='%(message)s')
logger=logging.getLogger(__name__)
try:
     import requests
except Exception as e:
          logger.info(str(e)+"\\n\xe7\xbc\xba\xe5\xb0\x91requests\xe6\xa8\xa1\xe5\x9d\x97, \xe8\xaf\xb7\xe6\x89\xa7\xe8\xa1\x8c\xe5\x91\xbd\xe4\xbb\xa4\xef\xbc\x9apip3 install requests\\n")
          sys.exit(1)
os.environ['no_proxy']='*'
requests.packages.urllib3.disable_warnings()
ver=905
def ql_login():
               path='/ql/config/auth.json'
               if os.path.isfile(path):
                         with open(path,"r")as file:
                                   auth=file.read()
                                   file.close()
                                   auth=json.loads(auth)
                                   username=auth["username"]
                                   password=auth["password"]
                                   token=auth["token"]
                                   if token=='':
                                        url="http://127.0.0.1:{0}/api/login".format(port)
                                        payload={"username":username,"password":password}
                                        headers={'Content-Type':'application/json'}
                                        try:
                                             res=requests.post(url=url,headers=headers,data=payload,verify=False)
                                             token=json.loads(res.text)['token']
                                        except:
                                             logger.info("\xe9\x9d\x92\xe9\xbe\x99\xe7\x99\xbb\xe5\xbd\x95\xe5\xa4\xb1\xe8\xb4\xa5, \xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe9\x9d\xa2\xe6\x9d\xbf\xe7\x8a\xb6\xe6\x80\x81!")
                                             sys.exit(1)
                                        else:
                                             return token
                                   else:
                                        return token
               else:
                    logger.info("\xe6\xb2\xa1\xe6\x9c\x89\xe5\x8f\x91\xe7\x8e\xb0auth\xe6\x96\x87\xe4\xbb\xb6, \xe4\xbd\xa0\xe8\xbf\x99\xe6\x98\xaf\xe9\x9d\x92\xe9\xbe\x99\xe5\x90\x97???")
                    sys.exit(0)
def get_wskey():
               if "JD_WSCK" in os.environ:
                    wskey_list=os.environ['JD_WSCK'].split('&')
                    if len(wskey_list)>0:
                         return wskey_list
                    else:
                         logger.info("JD_WSCK\xe5\x8f\x98\xe9\x87\x8f\xe6\x9c\xaa\xe5\x90\xaf\xe7\x94\xa8")
                         sys.exit(1)
               else:
                    logger.info("\xe6\x9c\xaa\xe6\xb7\xbb\xe5\x8a\xa0JD_WSCK\xe5\x8f\x98\xe9\x87\x8f")
                    sys.exit(0)
def get_ck():
               if "JD_COOKIE" in os.environ:
                    ck_list=os.environ['JD_COOKIE'].split('&')
                    if len(ck_list)>0:
                         return ck_list
                    else:
                         logger.info("JD_COOKIE\xe5\x8f\x98\xe9\x87\x8f\xe6\x9c\xaa\xe5\x90\xaf\xe7\x94\xa8")
                         sys.exit(1)
               else:
                    logger.info("\xe6\x9c\xaa\xe6\xb7\xbb\xe5\x8a\xa0JD_COOKIE\xe5\x8f\x98\xe9\x87\x8f")
                    sys.exit(0)
def check_ck(ck):
               if "QL_WSCK" in os.environ:
                    logger.info("\xe4\xb8\x8d\xe6\xa3\x80\xe6\x9f\xa5\xe8\xb4\xa6\xe5\x8f\xb7\xe6\x9c\x89\xe6\x95\x88\xe6\x80\xa7\\n--------------------\\n")
                    return False
               else:
                    url='https://wq.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New&callSource=mainorder'
                    headers={'Cookie':ck,'Referer':'https://home.m.jd.com/myJd/home.action','User-Agent':ua,}
                    try:
                         res=requests.get(url=url,headers=headers,verify=False,timeout=10)
                         if res.status_code==200:
                              code=int(json.loads(res.text)['retcode'])
                              pin=ck.split(";")[1]
                              if code==0:
                                   logger.info(str(pin)+";\xe7\x8a\xb6\xe6\x80\x81\xe6\xad\xa3\xe5\xb8\xb8\\n")
                                   return True
                              else:
                                   logger.info(str(pin)+";\xe7\x8a\xb6\xe6\x80\x81\xe5\xa4\xb1\xe6\x95\x88\\n")
                                   return False
                         else:
                              logger.info("JD\xe6\x8e\xa5\xe5\x8f\xa3\xe9\x94\x99\xe8\xaf\xaf, \xe5\x88\x87\xe6\x8d\xa2\xe7\xac\xac\xe4\xba\x8c\xe6\x8e\xa5\xe5\x8f\xa3")
                              url='https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'
                              headers={'Cookie':ck,'User-Agent':ua,}
                              res=requests.get(url=url,headers=headers,verify=False,timeout=30)
                         if res.status_code==200:
                              code=int(json.loads(res.text)['retcode'])
                              pin=ck.split(";")[1]
                              if code==0:
                                   logger.info(str(pin)+";\xe7\x8a\xb6\xe6\x80\x81\xe6\xad\xa3\xe5\xb8\xb8\\n")
                                   return True
                              else:
                                   logger.info(str(pin)+";\xe7\x8a\xb6\xe6\x80\x81\xe5\xa4\xb1\xe6\x95\x88\\n")
                                   return False
                    except:
                         logger.info("\\nJD\xe6\x8e\xa5\xe5\x8f\xa3\xe9\x94\x99\xe8\xaf\xaf! ")
                         logger.info("\xe8\x84\x9a\xe6\x9c\xac\xe9\x80\x80\xe5\x87\xba")
                         sys.exit(1)
def getToken(wskey):
                    headers={'cookie':wskey,'User-Agent':ua,'content-type':'application/x-www-form-urlencoded; charset=UTF-8','charset':'UTF-8','accept-encoding':'br,gzip,deflate'}
                    params={'functionId':'genToken','clientVersion':'10.1.2','client':'android','uuid':uuid,'st':st,'sign':sign,'sv':sv}
                    url='https://api.m.jd.com/client.action'
                    data='body=%7B%22action%22%3A%22to%22%2C%22to%22%3A%22https%253A%252F%252Fplogin.m.jd.com%252Fcgi-bin%252Fm%252Fthirdapp_auth_page%253Ftoken%253DAAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg%2526client_type%253Dandroid%2526appid%253D879%2526appup_type%253D1%22%7D&'
                    try:
                         res=requests.post(url=url,params=params,headers=headers,data=data,verify=False,timeout=10)
                         res_json=json.loads(res.text)
                         tokenKey=res_json['tokenKey']
                    except:
                    try:
                         res=requests.post(url=url,params=params,headers=headers,data=data,verify=False,timeout=20)
                         res_json=json.loads(res.text)
                         tokenKey=res_json['tokenKey']
                         return appjmp(wskey,tokenKey)
                    except:
                         logger.info("WSKEY\xe8\xbd\xac\xe6\x8d\xa2\xe6\x8e\xa5\xe5\x8f\xa3\xe5\x87\xba\xe9\x94\x99, \xe8\xaf\xb7\xe7\xa8\x8d\xe5\x90\x8e\xe5\xb0\x9d\xe8\xaf\x95, \xe8\x84\x9a\xe6\x9c\xac\xe9\x80\x80\xe5\x87\xba")
                         sys.exit(1)
                    else:
                         return appjmp(wskey,tokenKey)
def appjmp(wskey,tokenKey):
                         headers={'User-Agent':ua,'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',}
                         params={'tokenKey':tokenKey,'to':'https://plogin.m.jd.com/cgi-bin/m/thirdapp_auth_page?token=AAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg','client_type':'android','appid':879,'appup_type':1,}
                         url='https://un.m.jd.com/cgi-bin/app/appjmp'
                         try:
                              res=requests.get(url=url,headers=headers,params=params,verify=False,allow_redirects=False,timeout=20)
                              res_set=res.cookies.get_dict()
                              pt_key='pt_key='+res_set['pt_key']
                              pt_pin='pt_pin='+res_set['pt_pin']
                              jd_ck=str(pt_key)+';'+str(pt_pin)+';'
                              wskey=wskey.split(";")[0]
                              if 'fake' in pt_key:
                                        logger.info(str(wskey)+"wskey\xe7\x8a\xb6\xe6\x80\x81\xe5\xa4\xb1\xe6\x95\x88\\n")
                                        return False,jd_ck
                              else:
                                   logger.info(str(wskey)+" wskey\xe7\x8a\xb6\xe6\x80\x81\xe6\xad\xa3\xe5\xb8\xb8\\n")
                                   return True,jd_ck
                         except:
                              logger.info("\xe6\x8e\xa5\xe5\x8f\xa3\xe8\xbd\xac\xe6\x8d\xa2\xe5\xa4\xb1\xe8\xb4\xa5, \xe9\xbb\x98\xe8\xae\xa4wskey\xe5\xa4\xb1\xe6\x95\x88\\n")
                              wskey="pt_"+str(wskey.split(";")[0])
                              return False,wskey
def get_sign():
               sign_bool=False
               url=str(base64.b64decode('aHR0cHM6Ly9oZWxsb2Rucy5jb2RpbmcubmV0L3Avc2lnbi9kL2pzaWduL2dpdC9yYXcvbWFzdGVyL3NpZ24=').decode())
               for i in range(3):
                    try:
                         res=requests.get(url=url,verify=False,timeout=20)
                    except requests.exceptions.ConnectTimeout:
                         logger.info("\\n\xe8\x8e\xb7\xe5\x8f\x96Sign\xe8\xb6\x85\xe6\x97\xb6, \xe6\xad\xa3\xe5\x9c\xa8\xe9\x87\x8d\xe8\xaf\x95!"+str(i))
                         time.sleep(1)
                    except requests.exceptions.ReadTimeout:
                         logger.info("\\n\xe8\x8e\xb7\xe5\x8f\x96Sign\xe8\xb6\x85\xe6\x97\xb6, \xe6\xad\xa3\xe5\x9c\xa8\xe9\x87\x8d\xe8\xaf\x95!"+str(i))
                         time.sleep(1)
                    except Exception as err:
                                             logger.info(str(err)+"\\n\xe6\x9c\xaa\xe7\x9f\xa5\xe9\x94\x99\xe8\xaf\xaf, \xe9\x80\x80\xe5\x87\xba\xe8\x84\x9a\xe6\x9c\xac!")
                                             sys.exit(1)
                                        else:
                                             sign_bool=True
                                             break
                                        if sign_bool:
                                             sign_list=json.loads(res.text)
                                             svv=sign_list['sv']
                                             stt=sign_list['st']
                                             suid=sign_list['uuid']
                                             jign=sign_list['sign']
                                             return svv,stt,suid,jign
                                        else:
                                             logger.info("\\nSign_Bool\xe5\x80\xbc\xe9\x94\x99\xe8\xaf\xaf, \xe9\x80\x80\xe5\x87\xba\xe8\x84\x9a\xe6\x9c\xac!")
def boom():
          ex=int(cloud_arg['code'])
          if ex!=200:
               logger.info("Check Failure")
               logger.info("--------------------\\n")
               sys.exit(0)
          else:
               logger.info("Verification passed")
               logger.info("--------------------\\n")
def update():
          up_ver=int(cloud_arg['update'])
          if ver>=up_ver:
               logger.info("\xe5\xbd\x93\xe5\x89\x8d\xe8\x84\x9a\xe6\x9c\xac\xe7\x89\x88\xe6\x9c\xac: "+str(ver))
               logger.info("--------------------\\n")
          else:
               logger.info("\xe5\xbd\x93\xe5\x89\x8d\xe8\x84\x9a\xe6\x9c\xac\xe7\x89\x88\xe6\x9c\xac: "+str(ver)+"\xe6\x96\xb0\xe7\x89\x88\xe6\x9c\xac: "+str(up_ver))
               logger.info("\xe5\xad\x98\xe5\x9c\xa8\xe6\x96\xb0\xe7\x89\x88\xe6\x9c\xac, \xe8\xaf\xb7\xe6\x9b\xb4\xe6\x96\xb0\xe8\x84\x9a\xe6\x9c\xac\xe5\x90\x8e\xe6\x89\xa7\xe8\xa1\x8c")
               logger.info("--------------------\\n")
               sys.exit(0)
def ql_check(port):
               sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
               sock.settimeout(2)
               try:
                    sock.connect(('127.0.0.1',port))
               except:
                    sock.close()
                    return False
               else:
                    sock.close()
                    return True
def serch_ck(pin):
               if all('\\u4e00\'<=char<=\'\\u9fff' for char in pin):
                    pin1=urllib.parse.quote(pin)
                    pin2=pin1.replace('%','%5C%25')
                    logger.info(str(pin)+"-->"+str(pin1))
               else:
                    pin2=pin.replace('%','%5C%25')
                    conn=http.client.HTTPConnection("127.0.0.1",5700)
                    payload=''
                    headers={'Authorization':'Bearer '+token}
                    url='/api/envs?searchValue={0}'.format(pin2)
                    conn.request("GET",url,payload,headers)
                    res=json.loads(conn.getresponse().read())
                    if len(res['data'])==0:
                         logger.info(str(pin)+"\xe6\xa3\x80\xe7\xb4\xa2\xe5\xa4\xb1\xe8\xb4\xa5\\n")
                         return False,1
                    elif len(res['data'])>1:
                         logger.info(str(pin)+"\xe5\xad\x98\xe5\x9c\xa8\xe9\x87\x8d\xe5\xa4\x8d, \xe5\x8f\x96\xe7\xac\xac\xe4\xb8\x80\xe6\x9d\xa1, \xe8\xaf\xb7\xe5\x88\xa0\xe9\x99\xa4\xe5\xa4\x9a\xe4\xbd\x99\xe5\x8f\x98\xe9\x87\x8f\\n")\n
                         key=res['data'][0]['value']
                         eid=res['data'][0]['_id']
                         return True,key,eid
                    else:
                         logger.info(str(pin)+"\xe6\xa3\x80\xe7\xb4\xa2\xe6\x88\x90\xe5\x8a\x9f\\n")
                         key=res['data'][0]['value']
                         eid=res['data'][0]['_id']
                         return True,key,eid
def ql_update(eid,n_ck):
                         url='http://127.0.0.1:{0}/api/envs'.format(port)
                         data={"name":"JD_COOKIE","value":n_ck,"_id":eid}
                         data=json.dumps(data)
                         res=json.loads(s.put(url=url,data=data).text)
                         if res['data']['status']==1: 
                              ql_enable(eid)
def ql_enable(eid):
                    url='http://127.0.0.1:{0}/api/envs/enable'.format(port)
                    data='["{0}"]'.format(eid)
                    res=json.loads(s.put(url=url,data=data).text)
                    if res['code']==200:
                         logger.info("\\n\xe8\xb4\xa6\xe5\x8f\xb7\xe5\x90\xaf\xe7\x94\xa8\\n--------------------\\n")
                         return True
                    else:
                         logger.info("\\n\xe8\xb4\xa6\xe5\x8f\xb7\xe5\x90\xaf\xe7\x94\xa8\xe5\xa4\xb1\xe8\xb4\xa5\\n--------------------\\n")
                         return False
def ql_disable(eid):
                    url='http://127.0.0.1:{0}/api/envs/disable'.format(port)
                    data='["{0}"]'.format(eid)
                    res=json.loads(s.put(url=url,data=data).text)
                    if res['code']==200:
                         logger.info("\\n\xe8\xb4\xa6\xe5\x8f\xb7\xe7\xa6\x81\xe7\x94\xa8\xe6\x88\x90\xe5\x8a\x9f\\n--------------------\\n")
                         return True
                    else:
                         logger.info("\\n\xe8\xb4\xa6\xe5\x8f\xb7\xe7\xa6\x81\xe7\x94\xa8\xe5\xa4\xb1\xe8\xb4\xa5\\n--------------------\\n")
                         return False
def ql_insert(i_ck):
                    data=[{"value":i_ck,"name":"JD_COOKIE"}]
                    data=json.dumps(data)
                    url='http://127.0.0.1:{0}/api/envs'.format(port)
                    s.post(url=url,data=data)
                    logger.info("\\n\xe8\xb4\xa6\xe5\x8f\xb7\xe6\xb7\xbb\xe5\x8a\xa0\xe5\xae\x8c\xe6\x88\x90\\n--------------------\\n")
def cloud_info():
               cloud_bool=False 
               url=str(base64.b64decode('aHR0cHM6Ly9oZWxsb2Rucy5jb2RpbmcubmV0L3Avc2lnbi9kL2pzaWduL2dpdC9yYXcvbWFzdGVyL2NoZWNrX2FwaQ==').decode())
               for i in range(3):
               try:
                    res=requests.get(url=url,verify=False,timeout=20).text
               except requests.exceptions.ConnectTimeout:
                    logger.info("\\n\xe8\x8e\xb7\xe5\x8f\x96\xe4\xba\x91\xe7\xab\xaf\xe5\x8f\x82\xe6\x95\xb0\xe8\xb6\x85\xe6\x97\xb6, \xe6\xad\xa3\xe5\x9c\xa8\xe9\x87\x8d\xe8\xaf\x95!"+str(i))
               except requests.exceptions.ReadTimeout:
                    logger.info("\\n\xe8\x8e\xb7\xe5\x8f\x96\xe4\xba\x91\xe7\xab\xaf\xe5\x8f\x82\xe6\x95\xb0\xe8\xb6\x85\xe6\x97\xb6, \xe6\xad\xa3\xe5\x9c\xa8\xe9\x87\x8d\xe8\xaf\x95!"+str(i))
               except Exception as err:
                    logger.info(str(err)+"\\n\xe6\x9c\xaa\xe7\x9f\xa5\xe9\x94\x99\xe8\xaf\xaf, \xe9\x80\x80\xe5\x87\xba\xe8\x84\x9a\xe6\x9c\xac!")
                    sys.exit(1)
               else:
                    cloud_bool=True
                    break
               finally:
                    time.sleep(1)
                    if cloud_bool:
                         global cloud_arg
                         cloud_arg=json.loads(res)
                    else:
                         logger.info("\xe6\x97\xa0\xe6\xb3\x95\xe8\x8e\xb7\xe5\x8f\x96\xe4\xba\x91\xe7\xab\xaf\xe9\x85\x8d\xe7\xbd\xae \xe7\xa8\x8b\xe5\xba\x8f\xe9\x80\x80\xe5\x87\xba\\n")
                         sys.exit(1)
                    if __name__=='__main__':
                         logger.info("\\n--------------------\\n")
                    if "QL_PORT" in os.environ:
                         try:
                              port=int(os.environ['QL_PORT'])
                         except:
                              logger.info("\xe5\x8f\x98\xe9\x87\x8f\xe6\xa0\xbc\xe5\xbc\x8f\xe6\x9c\x89\xe9\x97\xae\xe9\xa2\x98...\\n\xe6\xa0\xbc\xe5\xbc\x8f: export QL_PORT=\\"\xe7\xab\xaf\xe5\x8f\xa3\xe5\x8f\xb7\\"")
                              sys.exit(1)
                    else:
                         port=5700
                    if not ql_check(port):
                         logger.info(str(port)+"\xe7\xab\xaf\xe5\x8f\xa3\xe6\xa3\x80\xe6\x9f\xa5\xe5\xa4\xb1\xe8\xb4\xa5, \xe5\xa6\x82\xe6\x9e\x9c\xe6\x94\xb9\xe8\xbf\x87\xe7\xab\xaf\xe5\x8f\xa3, \xe8\xaf\xb7\xe5\x9c\xa8\xe5\x8f\x98\xe9\x87\x8f\xe4\xb8\xad\xe5\xa3\xb0\xe6\x98\x8e\xe7\xab\xaf\xe5\x8f\xa3 \\n\xe5\x9c\xa8config.sh\xe4\xb8\xad\xe5\x8a\xa0\xe5\x85\xa5 export QL_PORT=\\"\xe7\xab\xaf\xe5\x8f\xa3\xe5\x8f\xb7\\"")
                         logger.info("\\n\xe5\xa6\x82\xe6\x9e\x9c\xe4\xbd\xa0\xe5\xbe\x88\xe7\xa1\xae\xe5\xae\x9a\xe7\xab\xaf\xe5\x8f\xa3\xe6\xb2\xa1\xe9\x94\x99, \xe8\xbf\x98\xe6\x98\xaf\xe6\x97\xa0\xe6\xb3\x95\xe6\x89\xa7\xe8\xa1\x8c, \xe5\x9c\xa8GitHub\xe7\xbb\x99\xe6\x88\x91\xe5\x8f\x91issus\\n--------------------\\n")
                         sys.exit(1)
                    else:
                         logger.info(str(port)+"\xe7\xab\xaf\xe5\x8f\xa3\xe6\xa3\x80\xe6\x9f\xa5\xe9\x80\x9a\xe8\xbf\x87\\n")
                         global cloud_arg
                         cloud_info()
                         update()
                         ua=cloud_arg['User-Agent']
                         boom()
                         sv,st,uuid,sign=get_sign()
                         token=ql_login() 
                         s=requests.session()
                         s.headers.update({"authorization":"Bearer "+str(token)})
                         s.headers.update({"Content-Type":"application/json;charset=UTF-8"})
                         wslist=get_wskey()
                         for ws in wslist:
                              wspin=ws.split(";")[0]
                              if "pin" in wspin:
                                        wspin="pt_"+wspin+";" 
                                        return_serch=serch_ck(wspin) 
                                        if return_serch[0]: 
                                             jck=str(return_serch[1]) 
                                             if not check_ck(jck): 
                                                  return_ws=getToken(ws) 
                                                  if return_ws[0]: 
                                                            nt_key=str(return_ws[1])
                                                            logger.info("wskey\xe8\xbd\xac\xe6\x8d\xa2\xe6\x88\x90\xe5\x8a\x9f\\n")
                                                                                     logger.info("--------------------\\n")
                                                                                           eid=return_serch[2] 
                                                                                                 ql_update(eid,nt_key) 
                                                                                                      else:\n
                                                                                                            logger.info(str(ws)+"wskey\xe5\xa4\xb1\xe6\x95\x88\\n")\n
                                                                                                                  eid=return_serch[2]\n
                                                                                                                        logger.info("\xe7\xa6\x81\xe7\x94\xa8\xe8\xb4\xa6\xe5\x8f\xb7"+str(wspin))\n
                                                                                                                              ql_disable(eid)\n
                                                                                                                                  else:\n
                                                                                                                                       logger.info(str(wspin)+"\xe8\xb4\xa6\xe5\x8f\xb7\xe6\x9c\x89\xe6\x95\x88")\n
                                                                                                                                            eid=return_serch[2]\n
                                                                                                                                                 ql_enable(eid)\n
                                                                                                                                                      logger.info("--------------------\\n")\n
                                                                                                                                                         else:\n
                                                                                                                                                             logger.info("wskey\xe6\x9c\xaa\xe7\x94\x9f\xe6\x88\x90pt_key\\n")\n
                                                                                                                                                                 return_ws=getToken(ws) \n
                                                                                                                                                                     if return_ws[0]:\n
                                                                                                                                                                          nt_key=str(return_ws[1])\n
                                                                                                                                                                               logger.info("wskey\xe8\xbd\xac\xe6\x8d\xa2\xe6\x88\x90\xe5\x8a\x9f\\n")\n
                                                                                                                                                                                    ql_insert(nt_key)\n
                                                                                                                                                                                      else:\n
                                                                                                                                                                                         logger.info("WSKEY\xe6\xa0\xbc\xe5\xbc\x8f\xe9\x94\x99\xe8\xaf\xaf\\n--------------------\\n")\n
                                                                                                                                                                                          logger.info("\xe6\x89\xa7\xe8\xa1\x8c\xe5\xae\x8c\xe6\x88\x90\\n--------------------")\n
                                                                                                                                                                                           sys.exit(0)\n