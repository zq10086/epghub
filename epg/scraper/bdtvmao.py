from epg.model import Channel, Program
from datetime import datetime, date, timezone
import requests
import json
from . import headers, tz_shanghai

def update(
    channel: Channel, scraper_id: str | None = None, dt: date = datetime.today().date()
) -> bool:
  channel_id = channel.id if scraper_id == None else scraper_id
    url = f"https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query={channel_id}&resource_id=12520&format=json"
    # time.sleep(1)  # 防止 被BAN
    try:
        res = requests.get(url, headers=headers, timeout=5)
    except:
        return False
    if res.status_code != 200:
        return False
    try:
        res.encoding = 'GBK'  # 尝试使用 GBK 编码
        content = res.content.decode('GBK')  # 手动解码响应内容
        programs_data = json.loads(content)['data'][0]['data']
    except:
        return False
    # Purge channel programs on this date
    channel.flush(dt)
    # Update channel programs on this date, if any
    if len(programs_data) == 0:
        return False
    temp_program = None
    for program in programs_data:
        title = program["title"]
        starttime_str = program['times', '']
        starttime = (
            datetime.strptime(starttime_str, "%Y/%m/%d %H:%M")
            .astimezone(tz_shanghai)        
        )
        if temp_program != None:
            temp_program.end_time = starttime
            channel.programs.append(temp_program)
        temp_program = Program(title, starttime, None, channel.id + "@tvmao.com")
    temp_program.end_time = datetime.strptime("00:00", "%H:%M").astimezone(
        tz_shanghai
    ).replace(year=dt.year, month=dt.month, day=dt.day) + timedelta(days=1)
    channel.programs.append(temp_program)
    return True