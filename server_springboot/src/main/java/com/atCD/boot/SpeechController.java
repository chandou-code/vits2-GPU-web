package com.atCD.boot;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.List;

@RestController
public class SpeechController {

    @GetMapping("/run")
    public ResponseEntity<byte[]> run(@RequestParam("text") String speakText,
                                      @RequestParam(value = "id_speaker", required = false) String idSpeaker,
                                      @RequestParam(value = "length", required = false, defaultValue = "1") float voiceLength,
                                      @RequestParam(value = "noise", required = false, defaultValue = "0.37") float voiceNoise,
                                      @RequestParam(value = "noisew", required = false, defaultValue = "0.2") float noisew) {

        if (speakText.length() > 250) {
            return ResponseEntity.badRequest().body("合成过长，250".getBytes());
        }

        // 处理speak_text中的换行符
        speakText = speakText.replace("\n ", "").replace("\n", "");

        // 构建请求URL
        String url = "https://genshinvoice.top/api?speaker=" + id2role2(Integer.parseInt(idSpeaker)) + "_ZH&text=" + speakText +
                "&format=wav&length=" + voiceLength + "&noise=" + voiceNoise + "&noisew=" + noisew + "&sdp=0.2&language=ZH";

        // 发起GET请求
        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<byte[]> response = restTemplate.getForEntity(url, byte[].class);

        // 返回音频文件流
        return ResponseEntity.ok()
                .header("Content-Disposition", "attachment; filename=speech.wav")
                .body(response.getBody());
    }

    // 定义id2role2方法
    private String id2role2(int id) {
        List<String> models = Arrays.asList("阿尔卡米", "凯瑟琳", "阿贝多", "云堇", "烟绯", "常九爷", "史瓦罗", "卡维", "雷电将军", "掇星攫辰天君",
                "枫原万叶", "希儿", "夏洛蒂", "符玄", "派蒙", "「白老先生」", "早柚", "阿守", "迈勒斯", "香菱", "元太",
                "刻晴", "陆景和", "珐露珊", "娜维娅", "「散兵」", "荒泷一斗", "玛格丽特", "纳比尔", "哲平", "戴因斯雷布",
                "萍姥姥", "欧菲妮", "式大将", "迪希雅", "回声海螺", "嘉良", "凯亚", "白术", "伦纳德", "林尼", "慧心",
                "埃舍尔", "莫娜", "瓦尔特", "行秋", "吴船长", "奥列格", "爱德琳", "班尼特", "深渊法师", "「女士」",
                "娜塔莎", "坎蒂丝", "纳西妲", "流浪者", "天目十五", "奥兹", "温迪", "希露瓦", "阿洛瓦", "琳妮特",
                "螺丝咕姆", "玛塞勒", "刃", "影", "阿扎尔", "埃德", "多莉", "停云", "康纳", "八重神子", "宛烟", "罗刹",
                "雷泽", "塞琉斯", "景元", "阿娜耶", "恕筠", "罗莎莉亚", "佩拉", "申鹤", "海芭夏", "anzai", "瑶瑶", "桑博",
                "知易", "托马", "胡桃", "阿圆", "陆行岩本真蕈·元素生命", "石头", "伊利亚斯", "米卡", "白露", "菲米尼",
                "阿祇", "九条镰治", "萨齐因", "鹿野院平藏", "星", "海妮耶", "晴霓", "荧", "旁白", "久利须", "斯坦利",
                "妮露", "魈", "钟离", "佐西摩斯", "天叔", "伊迪娅", "玛乔丽", "柊千里", "霍夫曼", "阿晃", "安西",
                "塞塔蕾", "阿巴图伊", "迈蒙", "青雀", "丽莎", "阿拉夫", "浮游水蕈兽·元素生命", "鹿野奈奈", "艾莉丝",
                "杜拉夫", "穹", "「大肉丸」", "舒伯特", "五郎", "帕姆", "萨赫哈蒂", "丹吉尔", "琴", "艾尔海森", "丹恒",
                "艾伯特", "银狼", "嘉玛", "莺儿", "「公子」", "赛诺", "巴达维", "安柏", "深渊使徒", "克罗索", "悦",
                "笼钓瓶一心", "北斗", "昆钧", "杰帕德", "艾丝妲", "宵宫", "珊瑚", "沙扎曼", "那维莱特", "帕斯卡", "拉齐",
                "珊瑚宫心海", "绿芙蓉", "卡芙卡", "迪卢克", "卡波特", "塔杰·拉德卡尼", "空", "黑塔", "驭空", "羽生田千鹤",
                "费斯曼", "「博士」", "久岐忍", "莫塞伊思", "诺艾尔", "莱依拉", "留云借风真君", "恶龙", "镜流", "爱贝尔",
                "虎克", "神里绫人", "达达利亚", "长生", "蒂玛乌斯", "彦卿", "埃泽", "埃尔欣根", "上杉", "重云", "阿兰",
                "辛焱", "拉赫曼", "言笑", "甘雨", "克列门特", "龙二", "田铁嘴", "迪奥娜", "姬子", "老孟", "凝光",
                "迪娜泽黛", "女士", "埃洛伊", "柯莱", "艾文", "西拉杰", "砂糖", "阿佩普", "芭芭拉", "布洛妮娅", "毗伽尔",
                "百闻", "大毫", "「信使」", "查尔斯", "左然", "绮良良", "半夏", "七七", "松浦", "莎拉", "埃勒曼", "三月七",
                "神里绫华", "夜兰", "丹枢", "博来", "大慈树王", "公输师傅", "提纳里", "芙宁娜", "托克", "素裳", "博易",
                "可可利亚", "青镞", "夏彦", "优菈", "可莉", "九条裟罗", "纯水精灵？", "菲谢尔", "克拉拉", "莫弈",
                "德沃沙克");


        if (id >= 0 && id < models.size()) {
            return models.get(id);
        } else {
            // 处理索引超出范围的情况，例如返回默认角色或抛出异常
            return "error";
        }

    }
}
