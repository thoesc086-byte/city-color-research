const zoneImages = {
  coast: "assets/chapel-aerial-blue.jpg",
  dune: "assets/ucca-dune-museum.jpg",
  art: "assets/lonely-library-grey.jpg",
  living: "assets/aranya-art-center.jpg",
  night: "assets/aranya-community.jpg"
};

const zoneResearch = {
  coast: "真实地图上靠海一侧包含沙滩、礼堂、海岸线和孤独图书馆的精神轴，视觉以日照白、海蓝和混凝土灰为核心。",
  dune: "沙丘生态带连接沙滩、海风、低矮植被与沙丘美术馆，色彩应服从自然基底，避免高彩度人工色。",
  art: "艺术社区组团由展览、阅读、灰色建筑体量和公共文化空间组成，适合以混凝土灰和木色建立安静的文化气质。",
  living: "度假生活街区承载酒店、住宅、社区商业、慢行与公共家具，需要比海岸核心区更温暖、更有人尺度。",
  night: "夜间活动界面服务音乐、市集、演出、剧场和夜游消费，需要独立深色系统承接灯光与活动传播。"
};

function c(key, name, hex, reason, source, use, image) {
  return { key, name, hex, reason, source, use, image };
}

const zones = {
  coast: {
    number: "01",
    title: "海岸精神轴",
    summary: "礼堂、海岸线、孤独图书馆共同形成阿那亚最具识别度的白、灰、蓝关系。",
    text: "以礼堂、海面、孤独图书馆为核心，控制为高明度、低彩度、强留白的海岸精神界面。",
    palettes: {
      primary: {
        label: "主色调",
        logic: "主色选择同一组暖白到浅灰白。原因是海岸精神轴的主体不是鲜艳色，而是礼堂、步道、海雾和沙面反光共同形成的高明度白色系。",
        colors: [
          c("coast-p01", "海雾白", "#F6F2EA", "取自海雾和高日照下的空气感，用来保证页面与建筑界面的留白。", "海雾、天空反光", "大面积背景、导则版面", zoneImages.coast),
          c("coast-p02", "礼堂白", "#ECE9DF", "取自白色礼堂主体，保留暖灰倾向，避免纯白刺眼。", "阿那亚礼堂", "建筑主体、导视底色", "assets/aranya-chapel-unsplash.jpg"),
          c("coast-p03", "步道白", "#E4E0D6", "来自通向礼堂的白色步道，比礼堂白更耐脏、更适合铺装。", "海边步道", "铺装、慢行路径", "assets/aranya-chapel-unsplash.jpg"),
          c("coast-p04", "贝壳白", "#DDD8CC", "来自沙滩中贝壳和干沙混合的浅白，连接建筑与沙地。", "沙滩贝壳与干沙", "墙面、低矮设施", zoneImages.coast),
          c("coast-p05", "浅浪灰", "#D5D2C8", "来自浪花退去后的浅灰反光，给白色系增加层次。", "浪花与湿沙反光", "铺装边界、分隔线", zoneImages.coast),
          c("coast-p06", "海风灰白", "#CBC8BF", "取自海风环境中的白墙阴影，不让白色系统过于单薄。", "白墙阴影", "建筑阴面、栏板", "assets/aranya-chapel-unsplash.jpg"),
          c("coast-p07", "混凝土浅灰", "#C2BEB4", "来自孤独图书馆的清水混凝土浅面，是白色系进入灰色系的过渡。", "孤独图书馆混凝土", "立面、基座", "assets/lonely-library-grey.jpg"),
          c("coast-p08", "礁影灰", "#B8B5AD", "来自海岸建筑阴影，适合作为白色体系中的压低色。", "建筑阴影", "阴影面、信息底板", "assets/lonely-library-grey.jpg"),
          c("coast-p09", "远岸灰", "#AEA9A0", "来自远处海岸线和阴天视感，承担弱对比边界。", "远岸与阴天海面", "次级文字底、栏杆", zoneImages.coast),
          c("coast-p10", "滩石灰", "#A49E94", "来自沙滩石与混凝土的中间灰，给系统增加耐久感。", "滩石、混凝土", "地面设施、台阶", "assets/lonely-library-grey.jpg"),
          c("coast-p11", "静默灰", "#99938A", "来自图书馆体量的静默感，作为主色系较深端。", "孤独图书馆阴影", "建筑基座、标识背板", "assets/lonely-library-grey.jpg"),
          c("coast-p12", "潮影灰", "#8D867D", "来自潮湿混凝土和背光墙面的深灰，是海岸白灰系统的收束色。", "潮湿混凝土、背光墙面", "深色基座、低明度标识", "assets/lonely-library-grey.jpg")
        ]
      },
      secondary: {
        label: "辅色",
        logic: "辅色选择同一组低彩度海蓝。原因是海岸轴需要海面和天空作为辅助识别，但蓝色不能压过白色建筑主体。",
        colors: [
          c("coast-s01", "晨雾蓝", "#B8CBD2", "来自清晨海天交界的浅蓝，用于柔和提示。", "清晨天空", "轻提示、图表底", zoneImages.coast),
          c("coast-s02", "浅海蓝", "#A5BEC8", "来自近岸浅水，比天空蓝更稳。", "近岸海水", "水岸导视", zoneImages.coast),
          c("coast-s03", "晨海蓝", "#8FAFBC", "来自航拍中的海面中间调，是核心辅助蓝。", "海面中间调", "信息层级、地图图形", zoneImages.coast),
          c("coast-s04", "潮汐蓝", "#789FAD", "来自退潮后较深的水色，用于强调但不过亮。", "潮汐水面", "二级导视", zoneImages.coast),
          c("coast-s05", "远海蓝", "#5F8796", "来自远海深一层的蓝灰，适合小面积。", "远海", "按钮、重点信息", zoneImages.coast),
          c("coast-s06", "深湾蓝", "#436D7C", "来自深水和阴影海面，作为辅色系最深端。", "深水海面", "深色文字背景", zoneImages.coast)
        ]
      },
      accent: {
        label: "点缀色",
        logic: "点缀色允许跨色系，只用于人群、活动和夜间节点，不能反向成为海岸建筑主色。",
        colors: [
          c("coast-a01", "船影黑", "#16242B", "来自海面船影和门洞暗部，用于极小面积压住画面。", "船影、门洞", "标识文字、暗色按钮", zoneImages.coast),
          c("coast-a02", "落日珊瑚", "#C76F58", "来自日落活动，给精神轴增加人气但不侵占建筑。", "日落与活动", "活动提示", "assets/sunset-people.jpg"),
          c("coast-a03", "海鸟白", "#F1EEE6", "来自海岸飞鸟和灯下白墙，用来做极轻的高光点。", "飞鸟、灯下白墙", "图标高光、悬浮提示", zoneImages.coast),
          c("coast-a04", "礁石褐", "#6B5648", "来自湿礁石和木平台暗部，补足海岸界面的材料锚点。", "礁石、木平台暗部", "栏杆节点、材料标注", zoneImages.coast),
          c("coast-a05", "救生橙", "#D08A4D", "来自救生设备和临时活动物料，只在安全提示中出现。", "救生设备、临时物料", "安全提示、临时导视", "assets/sunset-people.jpg")
        ]
      }
    }
  },
  dune: {
    number: "02",
    title: "沙丘生态带",
    summary: "沙丘、美术馆、植被和海面构成自然底色，是阿那亚最适合做大面积基底的区域。",
    text: "以沙丘米和海植绿建立自然本底，辅以晨海蓝，控制所有景观设施不过度商业化。",
    palettes: {
      primary: {
        label: "主色调",
        logic: "主色选择沙丘米同色系。原因是沙丘生态带的最大视觉面积来自沙滩、沙丘、低矮铺装和沙丘美术馆外部。",
        colors: [
          c("dune-p01", "干沙白", "#EFE6D5", "取自日照下的干沙高明度部分，用于最轻背景。", "干沙高光", "背景、浅墙面", zoneImages.dune),
          c("dune-p02", "细沙米", "#E6DAC5", "来自沙面主色，是沙丘带最稳定的大面积色。", "沙滩主面", "铺装、墙面", zoneImages.dune),
          c("dune-p03", "沙丘米", "#D8C6AA", "来自沙丘美术馆周边沙地，作为核心主色。", "沙丘与美术馆边界", "景观基底", zoneImages.dune),
          c("dune-p04", "风蚀米", "#CFBA9E", "来自风吹形成的沙纹阴影，增加自然起伏。", "沙纹阴影", "铺装分区", zoneImages.dune),
          c("dune-p05", "湿沙褐米", "#C3AE91", "取自近海湿沙，适合更耐脏的地面。", "湿沙", "地面、低墙", zoneImages.dune),
          c("dune-p06", "芦苇米", "#B9A482", "来自海边枯草和芦苇，连接沙地与植被。", "枯草、芦苇", "景观设施", zoneImages.dune),
          c("dune-p07", "贝壳米", "#DCCDB8", "来自沙中贝壳的偏白米色，用于浅色过渡。", "贝壳与沙", "座椅、导视底", zoneImages.dune),
          c("dune-p08", "浅陶土米", "#C8A889", "来自沙丘边界土色，比普通米色更有地貌感。", "土壤边界", "低矮构筑物", zoneImages.dune),
          c("dune-p09", "砂岩色", "#B99B7C", "来自砂岩和粗沙颗粒，提供材料质感。", "砂岩、粗沙", "材料样板", zoneImages.dune),
          c("dune-p10", "沙丘阴影", "#A88D72", "来自沙丘阴影的深米褐，作为主色最深端。", "沙丘阴影", "台阶、边界", zoneImages.dune),
          c("dune-p11", "沙脊褐", "#967D66", "来自沙丘脊线阴影，适合小面积承重部位。", "沙丘脊线", "基座、栏杆", zoneImages.dune),
          c("dune-p12", "沉沙褐", "#806A56", "来自湿沙深色端，控制主色系的最低明度。", "湿沙深处", "地面收边", zoneImages.dune)
        ]
      },
      secondary: {
        label: "辅色",
        logic: "辅色选择海植绿同色系。原因是沙丘带的生态边界由滨海植被、防风林和草坡构成，绿色是自然系统而不是装饰色。",
        colors: [
          c("dune-s01", "浅草绿", "#AAB99A", "来自沙地边缘浅草，适合柔和过渡。", "浅草坡", "生态说明底色", zoneImages.dune),
          c("dune-s02", "盐生绿", "#92A582", "来自耐盐植被，带灰度不刺眼。", "滨海植被", "景观标识", zoneImages.dune),
          c("dune-s03", "海植绿", "#748C70", "来自沙丘边界主植被色，是核心辅色。", "沙丘植被", "设施、节点", zoneImages.dune),
          c("dune-s04", "防风林绿", "#58745F", "来自防风林暗部，增强生态厚度。", "防风林", "公共家具", zoneImages.dune),
          c("dune-s05", "松影绿", "#435E4D", "来自树影和密植区，适合深色标识。", "树影", "深色导视", zoneImages.dune),
          c("dune-s06", "苔影绿", "#344C3F", "来自潮湿植被暗部，用于小面积压低。", "潮湿植被", "边界、文字", zoneImages.dune)
        ]
      },
      accent: {
        label: "点缀色",
        logic: "点缀色来自海水和日落，只用于观景节点与活动标记，避免破坏生态连续性。",
        colors: [
          c("dune-a01", "水线蓝", "#6F9BB0", "来自沙滩与海交界线，提示水岸方向。", "海岸水线", "水岸节点", zoneImages.dune),
          c("dune-a02", "日照橙", "#C98A5D", "来自沙丘日落暖光，适合少量活动点。", "日落暖光", "活动标记", "assets/sunset-people.jpg"),
          c("dune-a03", "海草深绿", "#344C3F", "来自沙丘背风面的密植被，用作生态边界的强调。", "背风面植被", "生态警示、步道边界", zoneImages.dune),
          c("dune-a04", "贝壳粉", "#D8A59A", "来自贝壳内侧和日落反光，作为柔和的游憩提示色。", "贝壳、晚霞反光", "亲子活动、休憩节点", zoneImages.dune),
          c("dune-a05", "潮痕墨", "#2E3F45", "来自退潮后湿沙里的深色潮痕，用于压住浅沙体系。", "湿沙潮痕", "说明牌文字、边界线", zoneImages.dune)
        ]
      }
    }
  },
  art: {
    number: "03",
    title: "艺术社区组团",
    summary: "艺术中心、展览、阅读和公共活动让阿那亚从自然场景进入文化场景。",
    text: "以灰、白、木建立展陈和阅读气质，少量使用落日橙提示活动入口与传播内容。",
    palettes: {
      primary: {
        label: "主色调",
        logic: "主色选择混凝土灰同色系。原因是艺术社区的建筑识别来自孤独图书馆、展陈空间和灰色体量，灰色应承担文化底色。",
        colors: [
          c("art-p01", "展墙白灰", "#EFEDE8", "来自展墙和自然光反射，适合展陈背景。", "展墙、天光", "展陈背景", zoneImages.art),
          c("art-p02", "石膏浅灰", "#E3E0DA", "来自室内浅灰面，避免白墙过冷。", "室内浅灰", "室内界面", zoneImages.art),
          c("art-p03", "纸本灰", "#D7D4CD", "来自图书和纸张阴影，连接阅读属性。", "书页、纸本", "信息底板", zoneImages.art),
          c("art-p04", "混凝土浅灰", "#CAC6BD", "来自图书馆清水混凝土浅面。", "混凝土墙面", "建筑立面", "assets/lonely-library-grey.jpg"),
          c("art-p05", "图书馆灰", "#B9B1A5", "来自孤独图书馆主体，是文化组团核心灰。", "孤独图书馆", "建筑主体", "assets/lonely-library-grey.jpg"),
          c("art-p06", "水泥灰", "#ABA398", "来自水泥肌理中间调，适合耐久材料。", "水泥肌理", "铺装、台阶", "assets/lonely-library-grey.jpg"),
          c("art-p07", "影廊灰", "#9C958C", "来自廊下阴影，增强空间深度。", "廊下阴影", "廊道、基座", "assets/lonely-library-grey.jpg"),
          c("art-p08", "铅笔灰", "#8E887F", "来自建筑图纸和手绘灰度，呼应艺术生产。", "图纸灰度", "图形系统", zoneImages.art),
          c("art-p09", "雕塑灰", "#7F7971", "来自雕塑和装置阴影，适合小面积。", "艺术装置", "展签、边界", zoneImages.art),
          c("art-p10", "墨影灰", "#6F6A63", "作为灰色主系最深端，控制空间沉静感。", "深阴影", "深色文字背景", zoneImages.art)
        ]
      },
      secondary: {
        label: "辅色",
        logic: "辅色选择木色同色系。原因是阅读、停留和社区家具需要温度，木色能把艺术建筑的冷灰拉回人尺度。",
        colors: [
          c("art-s01", "浅木皮", "#C7AA86", "来自浅木饰面，用于温和过渡。", "浅木饰面", "室内家具", zoneImages.living),
          c("art-s02", "阅读木", "#B48F68", "来自阅读空间和座椅，是核心辅色。", "阅读空间木材", "座椅、扶手", zoneImages.living),
          c("art-s03", "栈道木", "#9B7656", "来自栈道与公共家具，适合室外。", "栈道、座椅", "公共家具", zoneImages.living),
          c("art-s04", "旧木褐", "#856346", "来自被海风侵蚀后的木材暗部。", "旧木材", "栏杆、边界", zoneImages.living),
          c("art-s05", "咖啡木", "#6F5139", "来自社区商业和室内停留区。", "室内商业木色", "商业小界面", zoneImages.living),
          c("art-s06", "深木影", "#57402E", "木色系最深端，用于小面积压低。", "木材阴影", "文字、标识", zoneImages.living)
        ]
      },
      accent: {
        label: "点缀色",
        logic: "点缀色服务展览、活动入口和夜间传播，应保持小面积、高识别。",
        colors: [
          c("art-a01", "展览橙", "#C76F58", "来自活动海报与日落，提示展览入口。", "活动传播", "海报、入口", "assets/sunset-people.jpg"),
          c("art-a02", "深海墨", "#16242B", "来自夜间场景，适合展陈暗底。", "夜间演出", "暗色展厅", zoneImages.night),
          c("art-a03", "纸签蓝", "#5F8796", "来自展签和海岸冷光，用于信息层级区分。", "展签、冷光反射", "展签、索引、链接", zoneImages.art),
          c("art-a04", "陶土红", "#9E5D4B", "来自艺术装置和陶质材料，补充文化组团的手作温度。", "陶质装置、手作材料", "工作坊、装置标记", zoneImages.living),
          c("art-a05", "馆灯金", "#D2A56D", "来自展厅暖光和夜间入口灯，作为文化活动的柔性召唤。", "展厅暖光、入口灯", "活动入口、票务提示", zoneImages.night)
        ]
      }
    }
  },
  living: {
    number: "04",
    title: "度假生活街区",
    summary: "街区、商业、公共家具和慢行空间需要比海岸核心区更温暖、更接近日常。",
    text: "以沙丘米、礼堂白作为日常底色，用阅读木和海植绿降低商业界面的突兀感。",
    palettes: {
      primary: {
        label: "主色调",
        logic: "主色选择暖米白同色系。原因是度假生活街区既需要海岸轻盈感，也要比礼堂轴更有人居温度。",
        colors: [
          c("living-p01", "晨光白", "#F2EDE3", "来自清晨街区墙面反光，用于最浅背景。", "晨光墙面", "住宅外墙", zoneImages.living),
          c("living-p02", "院墙白", "#EAE2D6", "来自小院和住宅浅墙，比礼堂白更生活化。", "社区院墙", "墙面、围合", zoneImages.living),
          c("living-p03", "居住米", "#E0D4C2", "来自街区主墙面，是生活区核心主色。", "生活街区墙面", "建筑主体", zoneImages.living),
          c("living-p04", "巷道米", "#D4C5B0", "来自步行巷道和铺装，用于人行空间。", "巷道铺装", "步道、台阶", zoneImages.living),
          c("living-p05", "庭院米", "#C8B79F", "来自庭院地面和低墙，适合耐久界面。", "庭院地面", "低墙、地面", zoneImages.living),
          c("living-p06", "浅驼米", "#BBA98F", "来自街区家具和遮阳阴影。", "街区家具", "小体量设施", zoneImages.living),
          c("living-p07", "屋檐米", "#AD9A82", "来自屋檐阴面和暖灰过渡。", "屋檐阴面", "檐口、边界", zoneImages.living),
          c("living-p08", "生活褐米", "#9F8A73", "来自日常使用后的材料痕迹。", "材料使用痕迹", "基座、台阶", zoneImages.living),
          c("living-p09", "慢行褐", "#907A63", "来自慢行路径和木质接触面。", "慢行路径", "路径收边", zoneImages.living),
          c("living-p10", "街角土褐", "#806B56", "生活区主色最深端，用于耐脏位置。", "街角地面", "商业基座", zoneImages.living)
        ]
      },
      secondary: {
        label: "辅色",
        logic: "辅色选择木褐同色系。原因是生活街区的设施、商业门头、座椅和栈道需要更亲近人的材料色。",
        colors: [
          c("living-s01", "浅栈木", "#C1A17C", "来自浅色栈道和座椅。", "栈道座椅", "公共家具", zoneImages.living),
          c("living-s02", "阅读木", "#AD835E", "来自阅读与停留空间。", "阅读空间", "室内外家具", zoneImages.living),
          c("living-s03", "门廊木", "#9B7656", "来自门廊和扶手，是生活区核心辅色。", "门廊扶手", "门头、扶手", zoneImages.living),
          c("living-s04", "深栈木", "#876346", "来自被海风压暗的木材。", "室外木材", "栏杆、地台", zoneImages.living),
          c("living-s05", "咖啡褐", "#735139", "来自社区商业的暖暗部。", "社区商业", "招牌底色", zoneImages.living),
          c("living-s06", "木影褐", "#5D412E", "木色最深端，用于小面积文字和边界。", "木材阴影", "文字、收边", zoneImages.living)
        ]
      },
      accent: {
        label: "点缀色",
        logic: "点缀色来自植被、活动与海水，帮助生活区识别功能节点。",
        colors: [
          c("living-a01", "庭院绿", "#58745F", "来自生活区绿化，柔化商业界面。", "庭院绿化", "绿化节点", zoneImages.dune),
          c("living-a02", "市集橙", "#C76F58", "来自市集活动，用于运营提示。", "市集活动", "活动标识", "assets/sunset-people.jpg"),
          c("living-a03", "水岸蓝", "#6F9BB0", "来自海岸方向，用于导向水岸。", "海岸方向", "导向系统", zoneImages.coast),
          c("living-a04", "咖啡焦糖", "#A56F45", "来自咖啡店、木门头和生活消费场景，强化街区烟火气。", "咖啡店、木门头", "商业小招牌、菜单重点", zoneImages.living),
          c("living-a05", "帆布红", "#B85F54", "来自市集遮阳布和活动织物，适合短期运营物料。", "市集织物、遮阳布", "市集摊位、节庆导视", "assets/sunset-people.jpg")
        ]
      }
    }
  },
  night: {
    number: "05",
    title: "夜间活动界面",
    summary: "音乐、市集、剧场和夜间社群活动需要一套独立但受控的深色与暖色系统。",
    text: "以夜游黑建立夜间底色，落日橙作为高识别点缀，晨海蓝用于低亮度信息层级。",
    palettes: {
      primary: {
        label: "主色调",
        logic: "主色选择深蓝黑同色系。原因是夜间活动需要承接舞台灯光、海岸暗部和人群剪影，纯黑过重，因此使用带蓝绿倾向的深色组。",
        colors: [
          c("night-p01", "暮海蓝黑", "#22343B", "来自傍晚海面暗部，深但不死黑。", "傍晚海面", "夜间背景", zoneImages.night),
          c("night-p02", "夜游黑", "#16242B", "来自夜间舞台和海边低照度，是核心主色。", "夜间活动", "活动底色", zoneImages.night),
          c("night-p03", "剧场墨蓝", "#1C2A32", "来自剧场暗场，适合承接文字。", "剧场暗场", "活动页面背景", zoneImages.night),
          c("night-p04", "深海影", "#10202A", "来自深水和灯光之外的暗部。", "深海暗部", "深色容器", zoneImages.night),
          c("night-p05", "幕布黑蓝", "#26323A", "来自舞台幕布和设备暗面。", "舞台设备", "舞台视觉", zoneImages.night),
          c("night-p06", "星夜灰蓝", "#303C43", "来自夜空较亮部分，适合二级深底。", "夜空", "二级背景", zoneImages.night),
          c("night-p07", "港湾暗蓝", "#0F2A35", "来自夜间海岸和港湾暗蓝。", "夜间海岸", "导航栏", zoneImages.night),
          c("night-p08", "低照度蓝", "#35454C", "来自低亮环境中的灰蓝。", "低照度环境", "弱分隔", zoneImages.night),
          c("night-p09", "人群剪影", "#111A1E", "来自演出人群剪影，作为最深端。", "人群剪影", "暗色文字、遮罩", zoneImages.night),
          c("night-p10", "灯后黑", "#2A2424", "来自舞台灯背后的暖黑，连接暖辅色。", "舞台灯背部", "深色卡片", zoneImages.night)
        ]
      },
      secondary: {
        label: "辅色",
        logic: "辅色选择琥珀橙同色系。原因是夜间业态依赖灯光、演出、市集和人群聚集，暖色负责可见度与运营温度。",
        colors: [
          c("night-s01", "灯晕米橙", "#E0B980", "来自灯光外沿的柔和暖色。", "灯光外晕", "弱提示", zoneImages.night),
          c("night-s02", "舞台琥珀", "#D69A5F", "来自舞台黄光，是夜间辅色核心。", "舞台灯光", "活动按钮", zoneImages.night),
          c("night-s03", "市集橙", "#C9814F", "来自市集和摊位灯光。", "市集灯光", "运营标识", zoneImages.night),
          c("night-s04", "落日橙", "#C76F58", "来自日落到夜间活动的过渡。", "日落活动", "传播点缀", "assets/sunset-people.jpg"),
          c("night-s05", "篝火铜", "#A85C40", "来自夜间暖光深处，适合小面积强调。", "暖光暗部", "强调标签", zoneImages.night),
          c("night-s06", "暗铜红", "#7C3E32", "暖色系最深端，避免高饱和红刺眼。", "暗红灯光", "警示与限量活动", zoneImages.night)
        ]
      },
      accent: {
        label: "点缀色",
        logic: "点缀色允许跳出深蓝黑和琥珀橙，用于舞台、票务、临时装置，不进入日间导则。",
        colors: [
          c("night-a01", "电光蓝", "#5C8FCA", "来自舞台冷光，增强夜间活动识别。", "舞台冷光", "票务、交互", zoneImages.night),
          c("night-a02", "剧场红", "#B9473F", "来自演出服装和舞台红光，必须小面积使用。", "舞台红光", "活动标记", zoneImages.night),
          c("night-a03", "月光白", "#F1EEE6", "来自夜间灯光下的白墙和文字，可保证可读性。", "灯下白墙", "文字、图标", zoneImages.night),
          c("night-a04", "霓虹青", "#4AA6A0", "来自夜间装置和舞台边缘冷光，用于临时互动节点。", "夜间装置、冷光边缘", "互动装置、状态提示", zoneImages.night),
          c("night-a05", "烟火紫", "#7E5A79", "来自演出烟雾和混合灯色，提供夜间活动的情绪层。", "舞台烟雾、混合灯光", "演出专题、节庆视觉", zoneImages.night)
        ]
      }
    }
  }
};

const zoneButtons = document.querySelectorAll(".zone");
const zoneSummary = document.querySelector("#zoneSummary");
const zoneTitle = document.querySelector("#zoneTitle");
const zoneText = document.querySelector("#zoneText");
const tonePanel = document.querySelector("#tonePanel");
const colorList = document.querySelector("#colorList");
const colorDetail = document.querySelector("#colorDetail");

let activeZone = "coast";

function allZoneColors(zoneKey) {
  const palettes = zones[zoneKey].palettes;
  return ["primary", "secondary", "accent"].flatMap((group) =>
    palettes[group].colors.map((color) => ({ ...color, group, groupLabel: palettes[group].label, groupLogic: palettes[group].logic }))
  );
}

function findColor(key) {
  for (const zoneKey of Object.keys(zones)) {
    const found = allZoneColors(zoneKey).find((color) => color.key === key);
    if (found) return found;
  }
  return allZoneColors(activeZone)[0];
}

function smallColorButton(color, active = false) {
  return `<button class="mini-color ${active ? "active" : ""}" data-color="${color.key}" style="--mini:${color.hex}">
    <span></span><strong>${color.name}</strong><small>${color.hex}</small>
  </button>`;
}

function isDarkColor(hex) {
  const value = hex.replace("#", "");
  const r = parseInt(value.slice(0, 2), 16);
  const g = parseInt(value.slice(2, 4), 16);
  const b = parseInt(value.slice(4, 6), 16);
  return (r * 299 + g * 587 + b * 114) / 1000 < 138;
}

function rgbTriplet(hex) {
  const value = hex.replace("#", "");
  return [
    parseInt(value.slice(0, 2), 16),
    parseInt(value.slice(2, 4), 16),
    parseInt(value.slice(4, 6), 16)
  ].join(" · ");
}

function uniqueList(items) {
  return [...new Set(items.filter(Boolean))];
}

function accentEvidenceImages(color) {
  const images = uniqueList([
    color.image,
    zoneImages[activeZone],
    color.key.includes("-a02") || color.key.includes("-a05") ? "assets/sunset-people.jpg" : "",
    color.key.includes("-a03") ? "assets/aranya-chapel-unsplash.jpg" : "",
    color.key.includes("-a04") ? "assets/aranya-community.jpg" : "",
    "assets/aranya-art-center.jpg"
  ]);
  const fallback = [
    "assets/aranya-chapel-unsplash.jpg",
    "assets/lonely-library-grey.jpg",
    "assets/ucca-dune-museum.jpg",
    "assets/aranya-community.jpg"
  ];
  return uniqueList([...images, ...fallback]).slice(0, 3);
}

function accentText(color) {
  const zone = zones[activeZone];
  return {
    why: `${color.name}不是从建筑主体中放大的主色，而是从“${color.source}”这类高识别、小面积场景里提取出来的信号色。它和${zone.title}的主色、辅色保持距离，作用是在人流、活动、导视或安全节点中制造短暂注意力，同时不破坏区域原本的低饱和底色。${color.reason}`,
    select: `选择 ${color.hex} 的原因，是它能够在${zone.title}的色彩系统里形成可见但受控的对比：远看能被识别，近看仍然保留阿那亚偏克制、偏自然的质感。它不适合铺满墙面或大面积景观设施，更适合承担“被看见一下”的任务。`,
    boundary: `建议使用在${color.use}。面积控制应明显低于主色和辅色：作为按钮、票务、临时导视、活动标签、边界线或图标高光时最有效；如果连续铺开，会削弱主色调的安静感，也会让区域视觉变得商业化。`
  };
}

function accentDetailBlock(color, index) {
  const text = accentText(color);
  const evidence = accentEvidenceImages(color);
  return `
    <section class="accent-detail-copy" id="accent-detail-${color.key}">
      <p class="accent-detail-no">NO. ${String(index + 1).padStart(2, "0")}</p>
      <p class="eyebrow">${color.groupLabel}</p>
      <h2>${color.name}</h2>
      <p class="detail-role">${color.use}</p>

      <div class="accent-detail-swatch" style="--detail:${color.hex};--detailText:${isDarkColor(color.hex) ? "#F4F1EA" : "#25302D"}">
        <strong>${color.hex}</strong>
        <span>RGB&nbsp;&nbsp;${rgbTriplet(color.hex)}</span>
        <span>${color.groupLabel} / ${color.use}</span>
      </div>

      <section class="accent-explain">
        <p class="accent-label">何为此色</p>
        <p>${text.why}</p>
      </section>

      <section class="accent-explain">
        <p class="accent-label">为何选择</p>
        <p>${text.select}</p>
      </section>

      <section class="accent-explain">
        <p class="accent-label">应用边界</p>
        <p>${text.boundary}</p>
      </section>

      <section class="accent-explain">
        <p class="accent-label">提取流程</p>
        <ol class="accent-process">
          <li><span>01</span><p>先定位 ${zones[activeZone].title} 的真实场景：${zoneResearch[activeZone]}</p></li>
          <li><span>02</span><p>从照片中锁定“${color.source}”，避开极端高光、阴影和后期滤镜。</p></li>
          <li><span>03</span><p>把稳定中间调与同区域主色、辅色并置测试，确认它只在${color.use}中成立，不反向变成大面积环境色。</p></li>
          <li><span>04</span><p>保留接近 ${color.hex} 的色值作为导则色，并记录照片来源、使用边界和与区域色系的关系。</p></li>
        </ol>
      </section>

      <section class="accent-explain">
        <p class="accent-label">代表样本（照片匹配）</p>
        <div class="accent-photo-evidence">
          ${evidence.map((image, photoIndex) => `
            <figure>
              <img src="${image}" alt="${color.name}照片证据 ${photoIndex + 1}">
              <figcaption>${photoIndex === 0 ? "直接取样照片" : photoIndex === 1 ? "区域环境参照" : "应用氛围补充"}</figcaption>
            </figure>
          `).join("")}
        </div>
      </section>
    </section>
  `;
}

function syncActiveColor(key) {
  document.querySelectorAll("[data-color]").forEach((button) => {
    button.classList.toggle("active", button.dataset.color === key);
  });
}

function scrollToAccentDetail(key) {
  requestAnimationFrame(() => {
    const target = document.querySelector(`#accent-detail-${key}`);
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}

function richColorCard(color, groupKey = "") {
  const textColor = isDarkColor(color.hex) ? "#F4F1EA" : "#1A1A1A";
  return `<button class="tone-color" data-color="${color.key}" style="--tone:${color.hex};--toneText:${textColor}">
    <span class="tone-chip"></span>
    <span class="tone-meta">
      <strong>${color.name}</strong>
      <small>${color.hex}</small>
      <em>${color.reason}</em>
    </span>
  </button>`;
}

function toneGridSettings(colorCount) {
  if (colorCount === 12) return { columns: 4, lastSpan: 1 };
  if (colorCount === 10) return { columns: 5, lastSpan: 1 };
  if (colorCount === 6) return { columns: 3, lastSpan: 1 };
  return { columns: Math.min(colorCount, 5), lastSpan: 1 };
}

function renderZone(zoneKey) {
  activeZone = zoneKey;
  const zone = zones[zoneKey];
  zoneButtons.forEach((button) => button.classList.toggle("active", button.dataset.zone === zoneKey));
  zoneSummary.innerHTML = `<span class="zone-number">${zone.number}</span><div><strong>${zone.title}</strong><small>${zone.summary}</small></div>`;
  zoneTitle.textContent = zone.title;
  zoneText.textContent = `${zone.text} ${zoneResearch[zoneKey]}`;

  tonePanel.innerHTML = ["primary", "secondary", "accent"].map((groupKey) => {
    const group = zone.palettes[groupKey];
    const grid = toneGridSettings(group.colors.length);
    const explanation = groupKey === "accent" ? "" : `<p class="tone-explanation">${group.logic}</p>`;
    return `<article class="tone-row expanded ${groupKey}">
      <div class="tone-heading">
        <h3>${group.label}</h3>
        <p>${group.logic}</p>
        <small>${group.colors.length} 个颜色</small>
      </div>
      <div class="tone-board">
        ${explanation}
        <div class="tone-colors" style="--toneColumns:${grid.columns};--lastSpan:${grid.lastSpan}">
          ${group.colors.map((color) => richColorCard(color, groupKey)).join("")}
        </div>
      </div>
    </article>`;
  }).join("");

  renderColorList(zoneKey);
  renderColorDetail(zone.palettes.primary.colors[0].key);
}

function renderColorList(zoneKey) {
  const colors = allZoneColors(zoneKey);
  colorList.innerHTML = colors.map((color, index) => smallColorButton(color, index === 0)).join("");
}

function renderColorDetail(key) {
  const color = findColor(key);
  colorDetail.classList.toggle("accent-detail", color.group === "accent");
  if (color.group === "accent") {
    const accentColors = allZoneColors(activeZone).filter((item) => item.group === "accent");
    colorDetail.innerHTML = `
      <div class="accent-detail-stack">
        ${accentColors.map((item, index) => accentDetailBlock(item, index)).join("")}
      </div>
    `;
    syncActiveColor(key);
    scrollToAccentDetail(key);
    return;
  }
  colorDetail.innerHTML = `
    <div class="detail-photo">
      <img src="${color.image}" alt="${color.name}来源照片">
    </div>
    <div class="detail-copy">
      <p class="eyebrow">${color.groupLabel}</p>
      <h2>${color.name}</h2>
      <p class="detail-role">${color.use}</p>
      <div class="detail-swatch" style="--detail:${color.hex}"><span>${color.hex}</span></div>
      <p class="detail-story">${color.reason}</p>
      <ol class="process-list">
        <li><strong>区域依据</strong><span>${zones[activeZone].title}：${zoneResearch[activeZone]}</span></li>
        <li><strong>观察对象</strong><span>${color.source}</span></li>
        <li><strong>提取方式</strong><span>从真实照片中避开极端高光和纯阴影，取稳定中间调，再按同色系归并到 ${color.groupLabel}。</span></li>
        <li><strong>选择原因</strong><span>${color.groupLogic}</span></li>
        <li><strong>应用边界</strong><span>${color.use}</span></li>
      </ol>
    </div>
  `;
  syncActiveColor(key);
}

document.addEventListener("click", (event) => {
  const zone = event.target.closest("[data-zone]");
  if (zone) renderZone(zone.dataset.zone);

  const color = event.target.closest("[data-color]");
  if (color) renderColorDetail(color.dataset.color);
});

renderZone("coast");
