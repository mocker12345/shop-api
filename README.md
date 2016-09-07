# Sakura
### author Congjie.Ran
![image](http://w.fa7.in/group2/M00/00/32/ChQyIFUFMcOAVJM8AABocueOMS4178.616x385.jpg)

## article

##### GET /article

参数|类型| 参数说明|是否必须（默认）
---|---|---|---
limit |int| 每页数量|否（12）
offset |int| 页码|否（1）
返回示例：

    {
      "data": [
        {
          "category": 0,
          "children": [],
          "content": "测试啊~~~~~~~~~~~~~~~~~~~~~~~~~~",
          "cover_url": "http://nd.com.cn!!!",
          "create_time": "2016-09-03T15:38:51+00:00",
          "good": 0,
          "id": 1,
          "price": [],
          "summary": "简介啊~~~~~~~~",
          "title": "test1"
        },
        {
          "category": 0,
          "children": [],
          "content": "测试啊~~~~~~~~~~~~~~~~~~~~~~~~~~",
          "cover_url": "http://nd.com.cn",
          "create_time": "2016-09-03T15:39:36+00:00",
          "good": 0,
          "id": 3,
          "price": [],
          "summary": "简介啊~~~~~~~~",
          "title": "test2"
        },
      ],
      "offset": 1,
      "total_page": 1
    }

##### GET /article/{article_id}
参数| 参数类型|参数说明|是否必须（默认）
---|---|---|---
article_id|url参数(int)|文章ID|是

返回示例

    //GET /article/11
    {
      "category": 0,
      "children": [
        {
          "category": 0,
          "cover_url": "http://nd.com.cn!!!",
          "id": 1,
          "summary": "简介啊~~~~~~~~",
          "title": "test1"
        }
      ],
      "content": "测试啊~~~~~~~~~~~~~~~~~~~~~~~~~~",
      "cover_url": "http://nd.com.cn!!!",
      "create_time": "2016-09-03T17:25:14+00:00",
      "good": 0,
      "id": 11,
      "price": [
        {
          "id": 5,
          "price": "110.00",
          "site_name": "淘宝",
          "site_url": "http://taobao.com"
        },
        {
          "id": 6,
          "price": "111.00",
          "site_name": "京东",
          "site_url": "http://jd.com"
        }
      ],
      "summary": "简介啊~~~~~~~~",
      "title": "test6"
    }

##### POST /article
参数| 参数类型|参数说明|是否必须（默认）
---|---|---|---
title|str|文章标题|是
cover_url|str|封面地址|是
summary|str|简介|是
good|int|赞|是（0）
category|int|文章分类|是
price（*）|list|价格列表|否
children（*）|list|关联文章|否

如果price存在：
参数| 参数类型|参数说明|是否必须（默认）
---|---|---|---
site_name|str|网站名称|是
site_url|str|购物地址|是
price|number|价格|是

如果children存在：
参数| 参数类型|参数说明|是否必须（默认）
---|---|---|---
id|int|子文章ID|是

请求示例

    {
      "category": 0,
      "children": [{
          "id":1
      }],
      "content": "测试啊~~~~~~~~~~~~~~~~~~~~~~~~~~",
      "cover_url": "http://nd.com.cn!!!",
      "good":0,
      "price": [{
          "site_name":"淘宝",
          "site_url":"http://taobao.com",
          "price":110

      },{
          "site_name":"京东",
          "site_url":"http://jd.com",
          "price":111
      }],
      "summary": "简介啊~~~~~~~~",
      "title": "test8"
    }

成功添加返回：

    {
      "code": 201,
      "success": true
    }

##### PUT /article/{article_id}
参数| 参数类型|参数说明|是否必须（默认）
---|---|---|---
article_id|url参数（int）|文章ID|是
id|int|文章ID|是

##### DELETE /atricle/{article_id}

参数| 参数类型|参数说明|是否必须（默认）
---|---|---|---
article_id|url参数（int）|文章ID|是

## category
##### GET /category
返回示例

    {
      "data": [
        {
          "id": 4,
          "name": "nd"
        },
        {
          "id": 5,
          "name": "nd1"
        },
        {
          "id": 6,
          "name": "nd2"
        },
        {
          "id": 1,
          "name": "rancongjie"
        },
        {
          "id": 2,
          "name": "zhongshan"
        }
      ]
    }
    
##### POST /category
参数| 参数类型|参数说明|是否必须（默认）
---|---|---|---
name|str|分类名称|是
请求示例

    {
      "name":"nd2"
    }
返回示例

    {
      "data": [
        {
          "id": 4,
          "name": "nd"
        },
        {
          "id": 5,
          "name": "nd1"
        },
        {
          "id": 6,
          "name": "nd2"
        },
        {
          "id": 1,
          "name": "rancongjie"
        },
        {
          "id": 2,
          "name": "zhongshan"
        }
      ]
    }


##### PUT /category/{category_id}
参数| 参数类型|参数说明|是否必须（默认）
---|---|---|---
category_id|url参数(int)|分类ID|是
name|str|分类名称|是

##### DELETE /category/{category_id}

参数| 参数类型|参数说明|是否必须（默认）
---|---|---|---
category_id|url参数(int)|分类ID|是


## commodity

##### GET /commodity
参数| 参数类型|参数说明|是否必须（默认）
---|---|---|---
limit |int| 每页数量|否（12）
offset |int| 页码|否（1）


##### POST /commodity
参数| 参数类型|参数说明|是否必须（默认）
---|---|---|---
title|str|商品名称|是
cover_url|str|封面图片|是
price|str|价格|是
summery|str|简介|是
buy_url|str|购买链接|是

