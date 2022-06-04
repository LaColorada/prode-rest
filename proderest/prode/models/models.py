from django.db import models



# Match prediction, league, team, match, players


# class Match(models.Model):
'''

'''

'''
    name = models.CharField(max_length=255)
    team1_score = models.PositiveIntegerField(default=0)
    team2_score = models.PositiveIntegerField(default=0)
'''    

'''
    relationship with user model
'''
'''
    user_prediction = 
'''

# class League(models.Model):
    '''
    name = models.CharField(max_length=255)
    teams = models.ManyToManyField(

    '''
# class Team(models.Model):
    '''
    name = models.CharField(max_length=255)
    players = models.ManyToManyField(
    '''
# class Player(models.Model):
    '''
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
    goals = models.ForeignKey(
    
    '''
