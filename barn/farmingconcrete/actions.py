from actstream import action


def new_garden_action(garden, added_by):
    action.send(added_by, verb='added garden', action_object=garden)
