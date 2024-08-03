# API 서버 과제

본 markdown 문서를 정상적으로 열람할 수 없는경우 다음의 instruction에 따라 웹브라우저를 통해 열람할 수 있습니다.
``` shell
$ pip install grip
$ grip README.md 
```

## 요구사항
### API 구현
아래의 [`API 스펙`](#api-스펙)을 만족하는 API서버를 작성합니다.

주어진 스펙이 명확하지 않거나 변경이 필요하다고 생각하는 점은 바꾸어도 좋습니다.
그 경우 합당한 이유를 같이 제시해주세요.  
예를 들어,
> `id`의 타입은 저장 용량을 고려하여 문자열보다 정수가 좋습니다. 따라서 정수타입으로 바꾸겠습니다.

위와 같이 이유를 제시하고 스펙을 변경해주시면 됩니다. 

![overview.png](https://user-images.githubusercontent.com/8840911/154299948-070e6ced-c046-4f1a-bbd2-ca7deaa798eb.png)


### 실행 가능한 코드
실행이 가능한 코드를 제출해주세요.  
하나의 실행 포인트가 있어도 좋고, 실행을 위한 안내 문서가 있어도 좋습니다.  
<ins>코드를 보는 사람이 제출된 코드를 실행할 수 있도록 가이드라인을 같이 제시해주세요.</ins>

## API 스펙
주어진 `Example Response`들은 대략적인 reponse 구조에 대한 sample입니다. 반드시 해당 양식에 맞출 필요는 없으며,
필요에 따라 field를 추가하거나 수정하여 구현하시면 되겠습니다.

### \[GET\] /symbol
사용 가능한 symbol 목록을 리턴합니다. 가능한 symbol수는 10개 이상으로 구현해주세요.

**Example Response**
``` json
{
    "symbol": [
        "BTCUSDT", "ETHUSDT", ...
    ]
}
```


### \[POST\] /store/{symbol}
요청받은 순간 백그라운드 프로세스를 실행하고 이후 [실행결과 확인 엔드포인트](#get-storeresultid)를 위해 사용할 `id`값을 리턴합니다.  
실행된 백그라운드 프로세스는 `symbol`에 해당하는 암호화폐의 실시간 가격을 1초 간격으로 10회 받아와서 각각의 시간과 함께 저장한 뒤 종료됩니다.

암호화폐의 가격을 가져오는 한 가지 방법은 다음 링크에서 제공하는 API를 사용하는 것입니다.  
가격조회는 public 채널로 열려있기 때문에 주어진 요건에 맞추어 요청을 보내면 별도의 인증절차 없이 데이터를 받아올 수 있습니다. 
> https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker

자유롭게 다른 거래소 및 다른 방법을 선택하여 구현하셔도 좋습니다.  

**Example Response**
``` json
{
    "id": "1234"
}
```


### \[GET\] /store/result/{id}
[가격조회 요청 엔드포인트](#post-storesymbol)로부터 받아온 `id`에 해당하는 '가격을 받아오는 백그라운드 프로세스'의 상태를 리턴합니다.
프로세스의 상태를 통해 프로세스가 성공 또는 실패했는지 알 수 있어야 합니다.

**Example Response**
``` json
{
    "status": "OK",
}
```


### \[GET\] /data
가장 최근에 받아온 10개의 데이터를 리턴합니다.

**Example Response**
``` json
[
    {
        "symbol": "BTCUSDT",
        "timestamp": "2022-02-09 14:36:11.643706",
        "price": "24432"
    },
    {
        "symbol": "ETHUSDT",
        "timestamp": "2022-02-09 14:33:55.223931",
        "price": "1123"
    },
    ...
]
```

**\[선택사항\]**  
최근 10개의 데이터를 리턴한 후, 다음 10개의 데이터를 받아올 수 있는 정보도 같이 리턴해보세요.
해당 정보를 사용해 다음 10개씩 계속 조회할 수 있는 Endpoint를 추가해보세요.

### \[GET\] /data/{symbol}
`symbol`에 대한 최근 10개의 데이터를 리턴합니다.

**Example Response**
``` json
[
    {
        "symbol": "BTCUSDT",
        "timestamp": "2022-02-09 14:36:11.643706",
        "price": "24432"
    },
    {
        "symbol": "BTCUSDT",
        "timestamp": "2022-02-09 14:31:23.537221",
        "price": "24532"
    },
    ...
]
```

### \[GET\] /data/{symbol}/max
`symbol`에 대한 최근 10개의 데이터에서 최대값을 리턴합니다.

**Example Response**
``` json
{
    "symbol": "BTCUSDT",
    "timestamp": "2022-02-09 14:31:23.537221",
    "price": "24532"
}
```

### GET /data/{symbol}/wmax/{window}
`symbol`에 대하여 최근 10개의 moving maximum(window size=`window`)을 리턴합니다.

**Moving maximum**  
[Moving average](https://en.wikipedia.org/wiki/Moving_average) 와 마찬가지로 
`window`크기를 기준으로 이동하는 구간에서 최대값을 구하면 됩니다.
Moving average는 해당 구간에서 평균을 계산한 값입니다.  
![](https://user-images.githubusercontent.com/8840911/154299243-b62057d4-c32c-417f-a69d-1af71d1c9dbb.png)

**Example Response**
``` json
[
    {
        "symbol": "BTCUSDT",
        "timestamp": "2022-02-09 14:31:23.537221",
        "price": "24532"
    },
    {
        "symbol": "BTCUSDT",
        "timestamp": "2022-02-09 14:31:23.537221",
        "price": "24532"
    },
    ...
]
```

**\[선택사항\]**  
만약 K개의 데이터에서 window size=N으로 (K-N+1)개의 moving maximum을 효율적으로 계산하려면 어떻게 하면 좋을지
코드로 구현하거나 서술해 주세요. 해법의 시간복잡도도 함께 제시해주세요.

## 추가 자율 구현
제시된 스펙에서 추가로 필요해보이는 기능을 구현해주세요. 자신의 강점을 보여줄 수 있는 기능이면 더욱 좋습니다.
