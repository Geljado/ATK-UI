#Standalone Functions

version = 2.0
last_edit = [2,1,2022,"00:31"]

def FuzzySearchTier(item_list:list, search_term:str, join:bool=False):

    temp_list = []

    #tier list; tier one has first search letter in it;
    tier1, tier2, tier3 = [], [], []

    for letter in search_term.lower():
        for item in item_list:
            if letter in item.lower():
                temp_list.append(item)
                
        item_list = temp_list
        temp_list = []

    #Sorting based on first letter
    for item in item_list:
        if search_term.lower() in item.lower() and item[:1].lower() == search_term[:1].lower():
            tier1.append(item)
        elif item[:1].lower() == search_term[:1].lower() or search_term.lower() in item.lower():
            tier2.append(item)
        else:
            tier3.append(item)

    #Sorting for consistent results
    tier1.sort()
    tier2.sort()
    tier3.sort()

    #check if join; Joining lists
    if join:
        #reuse of variable, don't get confused
        item_list = []
        for item in tier1:
            item_list.append(item)
        for item in tier2:
            item_list.append(item)
        for item in tier3:
            item_list.append(item)
        return item_list
    else:
        return tier1,tier2,tier3

def ans2bool(answer):
    if answer == "yes":
        return True
    else:
        return False
 
