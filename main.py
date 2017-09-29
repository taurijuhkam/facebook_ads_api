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
from facebookads.adobjects.targeting import Targeting
from facebookads.adobjects.ad import Ad
from facebookads.adobjects.adimage import AdImage
from facebookads.adobjects.adcreative import AdCreative
from facebookads.adobjects.targetinggeolocation import TargetingGeoLocation
from example import example_dict

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
            'Either daily_budget or lifetime_budget must be defined!'
            )
        elif not campaign_data.get('end_time'):
            raise TypeError(
            'When using lifetime_budget, end_time must be defined!'
            )
        elif not campaign_data.get('campaign_name'):
            raise TypeError(
            'Campaign name cannot be empty!'
            )
        elif not campaign_data.get('ad_set_name'):
            raise TypeError(
            'Ad set name cannot be empty!'
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

        # Returns campaign id, it seems. Why do it via AdSet, dunno
        campaign_id = campaign[AdSet.Field.id]

    return campaign_id

def create_ad_set(campaign_data, account, campaign_id):
    """Creates an ad set and targeting for the campaign.
    
    Args:
        campaign_data (dict): A dict with campaign data, parsed from JSON
        account (str): Account where to upload the campaign
        campaign_id (str): Campaign id where to upload the Ad set
    """
    # Setup Ad set
    ad_set = AdSet(parent_id=account)
    ad_set[AdSet.Field.campaign_id] = campaign_id
    ad_set[AdSet.Field.name] = campaign_data.get('ad_set_name')
    ad_set[AdSet.Field.optimization_goal] = getattr(AdSet.OptimizationGoal,
                                                    campaign_data.get('optimization_goal'))
    ad_set[AdSet.Field.billing_event] = getattr(AdSet.BillingEvent,
                                                campaign_data.get('billing_event'))
    ad_set[AdSet.Field.is_autobid] = campaign_data.get('automatic_bidding')

    if campaign_data.get('daily_budget'):
        ad_set[AdSet.Field.daily_budget] = campaign_data.get('daily_budget')
    else:
        ad_set[AdSet.Field.lifetime_budget] = campaign_data.get('lifetime_budget')
    if campaign_data.get('end_time'):
        ad_set[AdSet.Field.end_time] = campaign_data.get('end_time')
    if campaign_data.get('start_time'):
        ad_set[AdSet.Field.start_time] = campaign_data.get('start_time')

    # Setup Targeting - maybe move to separate function
    # targeting is a dict!
    targeting = {}
    targeting[Targeting.Field.geo_locations] = {
        'countries': [campaign_data.get('country')]
    }
    if campaign_data.get('max_age'):
        targeting[Targeting.Field.age_max] = campaign_data.get('max_age')
    if campaign_data.get('min_age'):
        targeting[Targeting.Field.age_min] = campaign_data.get('min_age')

    #TODO: Language, region, Placements?
    #

    # Attach targeting to Ad set
    ad_set[AdSet.Field.targeting] = targeting

    ad_set.remote_create()


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

    print("\nRunning validations...")
    # Initial validations
    validate(campaign_data)

    print("\nUploading campaign...")
    # Get existing or create a new campaign
    campaign_id = create_campaign(campaign_data, account)
    print('Campaign uploaded!')
    # Create Ad set
    print("\nUploading AdSet...")
    create_ad_set(campaign_data, account, campaign_id)
    print('Ad set uploaded!')


def main():
    test_campaign_upload(example_dict, ACCOUNT)

if __name__ == '__main__':
    main()
