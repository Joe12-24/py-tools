import re

old_table_name = "OTC.LCODER3"
new_table_name = "OTC142.LCODER3"
content = '<?xml version="1.0" encoding="UTF-8" ?>\n<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >\n<mapper namespace="com.linkstec.lmspcom.auth.mapper.UserMapper">\n\t<update id="markDeleteById" parameterType="long">\n\t\tupdate OTC.L_USER3_sh SET LCODER_UPDATE_TIME = sysdate,\nOTC142.L_USER3_sh\nOTC142.L_USER3\n\t\tSET LCODER_UPDATE_TIME = sysdate,\n\t\t1=1\n\t\twhere 1=1\n\t\t<if>\n\t\tand b=1\n\t\t</if>\n\t</update>\n\t\n\t<delete id="deleteUserByIds" parameterType="map">\n\t\tdelete from  OTC142.L_USER3 <where> </where> \n\t\t\n\t</delete>\n<delete id="ZxDel" parameterType="com. Linkstec.newmall.dto.GJ2020fixedListInDto">\ndelete from otc.GJ_PRO_SELECT_100\nwhere TAB_id = #{ID} or ID = #{ID}\n</delete>\n\t\n\t<insert id="deleteUserByIds" parameterType="map">\n\t\t<!--update -->\n\t\tinsert into  OTC142.L_USER3 vaules()\n\t\t\n\t</insert>\n\n\t<delete id="deleteUserByIds" parameterType="map">\n\t\tdelete \n\t\t\tfrom \n\t\t\tOTC142.L_USER3 \n\t\t\t\n\t\t\twhere\n\t\t\n\t</delete>\n\t\n\t<update id="markDeleteByIds" parameterType="map">\n\t\t\tupdate OTC142.L_USER3_SET_TT\n\t\t\tset LCODER_UPDATE_TIME = sysdate \n\t\t\t\t\n\t\t\twhere 1=1\n\t</update>\n\t\n\t<insert id="deleteByMemberId" parameterType="long">\n\t\tinsert into  otc.L_USER values   member_id = #{_parameter}\n\t</insert>\n\t\n\t<update id="markDeleteById" parameterType="long">\n\t\tupdate otc.L_USER1 \n\t\tSET LCODER_UPDATE_TIME = sysdate, L1=1\n\t\t<foreach>\n\t\t</foreach>\n\t\t\n\t</update>\n\n\t\n\n</mapper>'

replaced_content = re.sub(r'\b%s\b' % old_table_name, new_table_name, content, flags=re.IGNORECASE)
print(replaced_content)
