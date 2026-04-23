fake={
    "2026-04-08":"available all day",
    "2026-04-09":"available between 1pm to 3pm",
    "2026-04-10":"available between 4pm to 9pm",
    "2026-04-11":"busy all day"
}
def calendar(date:str):
    """returns availablity of Jeff for tennis  match based on given date
    Args: date: str in format 'YYYY-MM-DD'
    Returns : dict of avilability details of Jeff
    """
    if date in fake:
        return {'status':'success','comment':fake[date]}
    return {'status':'input-needed','comment':'please try another date'}