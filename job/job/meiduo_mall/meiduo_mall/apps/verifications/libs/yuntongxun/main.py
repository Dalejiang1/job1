from yuntongxun.ccp_sms import CCP
import random

ccp = CCP()

num = random.randrange(0,999999)
sms_code = "%06d"% num

ccp.send_template_sms(
    '13066912819',
    [sms_code,5],
)