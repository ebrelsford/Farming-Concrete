from actstream import action


def download_garden_report_action(user, garden):
    action.send(user, verb='downloaded garden report', action_object=garden)
 

def download_garden_spreadsheet_action(user, garden):
    action.send(user, verb='downloaded garden spreadsheet',
                action_object=garden)
 

def download_garden_group_spreadsheet_action(user, garden_group):
    action.send(user, verb='downloaded garden group spreadsheet',
                action_object=garden_group)
