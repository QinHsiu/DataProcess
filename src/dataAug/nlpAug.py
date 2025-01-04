import json
import re
import random


# 题目完整性：0.1、0.3、0.5、0.8、0.9 1.0
# 公式正确性：0.1、0.3、0.5、0.8、1.0
# 是否可以解题：0.1、0.3、0.5、0.8、1.0
# 题目冗余性：0.1、0.3、0.5、0.8、1.0
# 题目连贯性：0.1、0.3、0.5、0.8、1.0

class TextAug():
    def __init__(self, *args, **kwargs):
        pass
    def cut_text(self,text, ratio, with_score=False):
        # 完整性
        score_dic = {'0.1':0.9
                     ,'0.2':0.8
                     ,'0.3':0.8
                     ,'0.4':0.5
                     ,'0.5':0.5
                     ,'0.6':0.3
                     ,'0.7':0.3
                     ,'0.8':0.1
                     ,'0.9':0.1
                     }
        # 冗余性为1，语义连贯性/可解性
        text_l = list(text)
        text_length = len(text_l)
        cut_length = int(text_length * eval(ratio))
        b_c = random.sample(list(range(text_length-cut_length)),1)[0]
        e_c = b_c + cut_length
        new_text = text[:b_c] + text[e_c:]
        if with_score:
            return [new_text, score_dic[ratio]]
        else:
            return new_text
    def reorder_text(self, text, ratio, with_score=False):
        # 语义连贯性
        score_dic = {'0.1':1.0
                     ,'0.2':0.8
                     ,'0.3':0.8
                     ,'0.4':0.5
                     ,'0.5':0.5
                     ,'0.6':0.3
                     ,'0.7':0.3
                     ,'0.8':0.1
                     ,'0.9':0.1
                     }
        # 可解性为1、完整性为1、冗余性为1
        text_l = list(text)
        text_length = len(text_l)
        reorder_length = int(text_length * eval(ratio))
        b_r = random.sample(list(range(text_length-reorder_length)),1)[0] 
        e_r = b_r + reorder_length
        new_text = text[:b_r] + text[b_r:e_r][::-1] + text[e_r:]
        if with_score:
            return [new_text, score_dic[ratio]]
        else:
            return new_text
        
    def mask_text(self, text, ratio, mask_text='N', with_score=False):
        # 语义连贯性，可解性
        score_dic = {'0.1':1.0
                     ,'0.2':0.8
                     ,'0.3':0.8
                     ,'0.4':0.5
                     ,'0.5':0.5
                     ,'0.6':0.3
                     ,'0.7':0.3
                     ,'0.8':0.1
                     ,'0.9':0.1
                     }
        # 完整性为1，冗余性为1
        text_l = list(text)
        text_length = len(text_l)
        mask_length = int(text_length * eval(ratio))
        b_m = random.sample(list(range(text_length-mask_length)),1)[0] 
        e_m = b_m + mask_length
        mask_texts = random.sample(text_l, mask_length)
        random.shuffle(mask_texts)
        mask_texts = ''.join(mask_texts)
        # mask_texts = mask_text * mask_length
        new_text = text[:b_m] + mask_texts + text[e_m:]
        if with_score:
            return [new_text, score_dic[ratio]]
        else:
            return new_text
        
    def insert_text(self, text, ratio, insert_text='N', with_score=False):
        # 冗余性、语义连贯性
        score_dic = {'0.1':1.0
                     ,'0.2':0.8
                     ,'0.3':0.8
                     ,'0.4':0.8
                     ,'0.5':0.5
                     ,'0.6':0.5
                     ,'0.7':0.3
                     ,'0.8':0.3
                     ,'0.9':0.1
                     }
        # 可解性为1、完整性为1
        text_l = list(text)
        text_length = len(text_l)
        insert_length = int(text_length * eval(ratio))
        # 0~l-1
        b_i = random.sample(list(range(text_length)),1)[0] 
        insert_texts = random.sample(text_l,insert_length)
        random.shuffle(insert_texts) 
        insert_texts = ''.join(insert_texts)
        # insert_texts = insert_text * insert_length
        
        new_text = text[:b_i] + insert_texts + text[b_i:]
        if with_score:
            return [new_text, score_dic[ratio]]
        else:
            return new_text
        
    def perturb_latex(self, text, perturb_type_list, ratio_str, with_score=False):
        '''请你编写一个函数，输入是一个文本，和一个0~1之间的浮点数，如果文本中不含latex语法，返回1，有latext语句，请你取出所有latext字段，然后实现四个子功能，对于latext字符实现增加字符、删除字符、改变字符、插入字符，操作的比例就是输入的第二个参数'''
        score_dic = {'0.1':1.0
                     ,'0.2':1.0
                     ,'0.3':0.8
                     ,'0.4':0.8
                     ,'0.5':0.5
                     ,'0.6':0.5
                     ,'0.7':0.3
                     ,'0.8':0.3
                     ,'0.9':0.1
                     }
        ratio = eval(ratio_str)
        # 正则表达式匹配LaTeX公式
        latex_pattern = re.compile(r'\$.*?\$', re.DOTALL)
        # 查找所有LaTeX字段
        latex_fields = latex_pattern.findall(text)
        if not latex_fields:
            if with_score:
                return [text, 1.0]
            else:
                return text
        perturbed_fields = []
        for field in latex_fields:
            perturbed_field = list(field)  # 转换为列表以便逐个字符处理
            num_chars = len(perturbed_field)
            
            # 增加字符
            if 'insert' in perturb_type_list:
                insert_count = int(num_chars * ratio)
                for _ in range(insert_count):
                    pos = random.randint(0, len(perturbed_field))
                    char_to_insert = chr(random.randint(33, 126))
                    perturbed_field.insert(pos, char_to_insert)
                    
            if 'delete' in perturb_type_list:
                # 删除字符
                delete_count = int(num_chars * ratio)
                for _ in range(delete_count):
                    if perturbed_field:  # 确保有字符可删
                        pos = random.randint(0, len(perturbed_field) - 1)
                        perturbed_field.pop(pos)
            if 'change' in perturb_type_list:
                # 改变字符
                change_count = int(num_chars * ratio)
                for _ in range(change_count):
                    if perturbed_field:  # 确保有字符可改
                        pos = random.randint(0, len(perturbed_field) - 1)
                        new_char = chr(random.randint(33, 126))
                        perturbed_field[pos] = new_char
   
            perturbed_fields.append(''.join(perturbed_field))
        
        # 替换原始文本中的LaTeX字段
        for original, perturbed in zip(latex_fields, perturbed_fields):
            text = text.replace(original, perturbed)
        
        if with_score:
            return [text,score_dic[ratio_str]]
        return text
        

class MultiTextAug(TextAug):
    def __init__(self, *args, **kwargs):
        pass
    
    def text_multi_aug(self, aug_dic):
        '''
            input:
                aug_dic, dic: a dic include multi text process operation, e.g., {'text_cut':'0.1','text_mask':'0.2','perturb_latex':{'perturb_type':['insert'],'ratio_str':'0.2'}}
            output:
                processed_text and score_dic, e.g., {'content':processed_text, 'score_dic':{'complete_score': '1', 'formula_right_score': '1', 'solve_score': '1', 'redundancy_score': '1', 'coherency_score': '1'},'ori_content':text}
        '''
        # {"问题": ["脱式计算。(9分)"],"条件": ["105 \\div 3 \\times 5","25 \\times (4 + 30)","(570 - 80) \\div 7"],"得分": {"完整性": "0.9","公式正确性": "0.8","可解性": "1","冗余性":"1","连贯性":"0.8"},"是否修正结果":"否"}
        pass
        
        
    

    
    
        
        
if __name__=='__main__':
    text_aug = TextAug()
    text = '如图,平行四边形ABCD中,点O为AC的中点,EF过O分别交AB,CD于E,F求证:S四AEFD=S四BEFC, $E=mc^2$ and another one $a^2 + b^2 = c^2$'
    ratio_l = [str(i/10) for i in range(1,10)]
    for r in ratio_l:
        perturb_type_list = ['insert','change','delete']
        new_text, score = text_aug.perturb_latex(text, perturb_type_list, r, True)
        print('ori_text: ',text)
        print('gen_text: ',new_text)
        print('score: ',score)
        print('')
        
        # new_text, score = text_aug.cut_text(text, r, True)
        # print('ori_text: ',text)
        # print('gen_text: ',new_text)
        # print('score: ',score)
        # print('')
        
        # new_text, score = text_aug.reorder_text(text, r, True)
        # print('ori_text: ',text)
        # print('gen_text: ',new_text)
        # print('score: ',score)
        # print('')

        # new_text, score = text_aug.mask_text(text, r,'M',True)
        # print('ori_text: ',text)
        # print('gen_text: ',new_text)
        # print('score: ',score)
        # print('')
    
     
    