# -*- coding: utf-8 -*-

"""
The main module, containing the basic flow
"""
import os
import conf
from pprint import pprint as pp
from facebookads import FacebookAdsApi
from facebookads import FacebookSession
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adset import AdSet
from facebookads.adobjects.campaign import Campaign

session = FacebookSession(conf.MY_APP_ID, conf.MY_APP_SECRET, conf.MY_ACCESS_TOKEN)
api = FacebookAdsApi(session)
ACCOUNT = 'act_' + conf.AD_ACCOUNT_ID
FacebookAdsApi.set_default_api(api)

def get_image_files():
    """Returns a list of paths of all the images in the current directory

    Returns:
        list: absolute paths of images in current directory
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    images = [img for img in os.listdir(current_dir) if img[-3:] in ['jpg', 'png']]
    image_paths = [os.path.join(current_dir, img) for img in images]
    return image_paths

example_dict = {
    'daily_budget': 500,  # 5.00 per day
    'lifetime_budget': '',
    'end_time': '',
    'campaign_id': '',
    'campaign_name': 'Test Campaign 02',
    'objective': 'link_clicks',
    # 'status': '',
}


def validate(campaign_data):
    """Performs validations on campaign_data and raises TyperError if something
    fails

    Args:
        campaign_data (dict): A dict with campaign data, parsed from JSON

    Raises:
        TypeError: Explanation as to which validation failed
    """
    if not campaign_data.get('daily_budget'):
        if not campaign_data.get('lifetime_budget'):
            raise TypeError(
            'Either daily_budget or lifetime_budget must be defined'
            )
        elif not campaign_data.get('end_time'):
            raise TypeError(
            'When using lifetime_budget, end_time must be defined'
            )


def create_campaign(campaign_data, account):
    """Creates a campaign, by default in paused status

    Args:
        campaign_data (dict): A dict with campaign data, parsed from JSON
        account (str): Account where to upload the campaign

    Returns:
        object: Campaign object?
    """
    # Existing campaing can be defined via campaign_id (or maybe name, not sure yet)
    if campaign_data.get('campaign_id'):
        campaign = Campaign(fbid=campaign_data.get('campaign_id'))[Campaign.Field.id]
    else:
        campaign = Campaign(parent_id=account)
        campaign[Campaign.Field.name] = campaign_data.get('campaign_name')
        campaign[Campaign.Field.objective] = getattr(Campaign.Objective,
                                                     campaign_data.get('objective'))
        # If not status is given, then default to Paused
        campaign[Campaign.Field.status] = getattr(Campaign.Status,
                                                  campaign_data.get('status', 'paused'))
        campaign.remote_create()

        # ??? What and why?
        campaign = campaign[AdSet.Field.id]

    return campaign

def test_campaign_upload(campaign_data, account):
    """
    Args:
        campaign_data (dict): parameters parsed from Json
        account (str): Account where to upload the campaing

    Returns:
        TYPE: Description
    """
    # Check if we're working with the correct account
    active_account = AdAccount(account)
    active_account.remote_read(fields=[AdAccount.Field.name])

    print('Uploading a campaign to %s' % active_account[AdAccount.Field.name])

    confirm = input('Do you want to continue? Y/N  --> ')
    if confirm not in ('y', 'Y'):
        print('Aborted campaign upload')
        return

    # Initial validations
    validate(campaign_data)

    # Get existing or create a new campaign
    create_campaign(campaign_data, account)



def main():
    test_campaign_upload(example_dict, ACCOUNT)

if __name__ == '__main__':
    main()
