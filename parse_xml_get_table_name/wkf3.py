import pandas as pd
import re  # 瀵煎叆姝ｅ垯琛ㄨ揪寮忓簱

# 璇诲彇鍘熷 Excel 鏂囦欢璺緞鍜岃緭鍑烘枃浠惰矾寰�
input_excel_file = '鍑屽織鎺ュ彛涓€瑙�.xlsx'  # 鏇挎崲涓轰綘鐨凟xcel鏂囦欢璺緞
output_excel_file = 'output_T寮€澶�17浣嶆暟瀛�.xlsx'  # 杈撳嚭鏂囦欢璺緞

# 浣跨敤 ExcelFile 鍔犺浇 Excel 鏂囦欢
xls = pd.ExcelFile(input_excel_file)

# 鍒涘缓涓€涓柊鐨� Excel 鏂囦欢锛屽苟璁剧疆 engine='openpyxl' 浠ユ敮鎸佸啓鍏�
with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
    for sheet_name in xls.sheet_names:
        # 璇诲彇姣忎釜 sheet 鐨勬暟鎹�
        df = pd.read_excel(xls, sheet_name=sheet_name)  # 璇诲彇鎵€鏈夊垪

        # 鍒濆鍖栫┖鍒楄〃鐢ㄤ簬瀛樺偍鎻愬彇鐨勫姛鑳藉彿
        extracted_numbers = []

        # 寰幆閬嶅巻姣忎竴琛屽拰姣忎竴鍒楀苟澶勭悊
        for index, row in df.iterrows():
            for value in row:
                # 鍙鐞嗗瓧绗︿覆绫诲瀷鐨勫€�
                if isinstance(value, str):
                    # 浣跨敤姝ｅ垯琛ㄨ揪寮忔煡鎵句互 'T' 寮€澶寸殑 7 浣嶆暟瀛�
                    match = re.search(r'T(\d{7})', value)
                    if match:
                        # 鎻愬彇鍔熻兘鍙峰苟鏍煎紡鍖�
                        extracted_numbers.append(f"T{match.group(1)}")

        # 鍒涘缓鏂扮殑 DataFrame 淇濆瓨鎻愬彇鍚庣殑鏁版嵁
        result_df = pd.DataFrame(extracted_numbers, columns=["鍔熻兘鍙�"])

        # 杈撳嚭鎻愬彇鏉℃暟
        print(f"Sheet '{sheet_name}' 涓彁鍙栧埌 {len(extracted_numbers)} 鏉′互 T 寮€澶寸殑 7 浣嶆暟瀛椼€�")

        # 灏嗙粨鏋滃啓鍏ュ埌鍚屼竴涓� sheet
        result_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"鎻愬彇鍚庣殑鏁版嵁宸蹭繚瀛樺埌 {output_excel_file} 涓€�")
# import pandas as pd
# import re  # 瀵煎叆姝ｅ垯琛ㄨ揪寮忓簱

# # 璇诲彇鍘熷 Excel 鏂囦欢璺緞鍜岃緭鍑烘枃浠惰矾寰�
# input_excel_file = '鍑屽織鎺ュ彛涓€瑙�.xlsx'  # 鏇挎崲涓轰綘鐨凟xcel鏂囦欢璺緞
# output_excel_file = 'output_T寮€澶�17浣嶆暟瀛楃粺璁�.xlsx'  # 杈撳嚭鏂囦欢璺緞

# # 浣跨敤 ExcelFile 鍔犺浇 Excel 鏂囦欢
# xls = pd.ExcelFile(input_excel_file)

# # 鍒濆鍖栫┖鍒楄〃鐢ㄤ簬瀛樺偍姣忎釜宸ヤ綔琛ㄧ殑鍚嶇О鍜屾彁鍙栫殑鏉℃暟
# summary_data = []

# # 閬嶅巻姣忎釜宸ヤ綔琛�
# for sheet_name in xls.sheet_names:
#     # 璇诲彇姣忎釜 sheet 鐨勬暟鎹�
#     df = pd.read_excel(xls, sheet_name=sheet_name)  # 璇诲彇鎵€鏈夊垪

#     # 鍒濆鍖栬鏁板櫒鐢ㄤ簬瀛樺偍鎻愬彇鐨勬潯鏁板拰鍐呭绛変簬 '鍔熻兘鍙�' 鐨勫崟鍏冩牸鏁伴噺
#     extracted_count = 0
#     func_num_count = 0

#     # 寰幆閬嶅巻姣忎竴琛屽拰姣忎竴鍒楀苟澶勭悊
#     for index, row in df.iterrows():
#         for value in row:
#             # 鍙鐞嗗瓧绗︿覆绫诲瀷鐨勫€�
#             if isinstance(value, str):
#                 # 妫€鏌ュ唴瀹规槸鍚︾瓑浜� '鍔熻兘鍙�'
#                 if value.strip() == '鍔熻兘鍙�':
#                     func_num_count += 1

#                 # 浣跨敤姝ｅ垯琛ㄨ揪寮忔煡鎵句互 'T' 寮€澶寸殑 7 浣嶆暟瀛�
#                  # 妫€鏌ュ崟鍏冩牸鍐呭鏄惁涓ユ牸绛変簬浠� 'T' 寮€澶寸殑 7 浣嶆暟瀛�
#                 if re.fullmatch(r'T\d{7}', value.strip()):
#                     extracted_count += 1  # 姣忔壘鍒颁竴涓尮閰嶏紝璁℃暟鍣ㄥ姞涓€

#     # 灏嗗伐浣滆〃鍚嶇О銆佹彁鍙栫殑鏉℃暟鍜屽姛鑳藉彿鍗曞厓鏍兼暟閲忔坊鍔犲埌 summary_data 鍒楄〃
#     summary_data.append({
#         "宸ヤ綔琛ㄥ悕绉�": sheet_name,
#         "鎻愬彇鏁伴噺": extracted_count,
#         "鍔熻兘鍙峰崟鍏冩牸鏁伴噺": func_num_count
#     })

# # 鍒涘缓鏂扮殑 DataFrame 淇濆瓨鎻愬彇鍚庣殑鏁版嵁
# summary_df = pd.DataFrame(summary_data)

# # 灏嗙粨鏋滃啓鍏ュ埌鏂扮殑 Excel 鏂囦欢涓殑鍚屼竴涓� sheet
# with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
#     summary_df.to_excel(writer, sheet_name='姹囨€荤粺璁�', index=False)

# print(f"鎻愬彇鍚庣殑鏁版嵁宸蹭繚瀛樺埌 {output_excel_file} 涓€�")
