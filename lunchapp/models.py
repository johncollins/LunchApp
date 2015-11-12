from django.db import models
from django.db.models import Q, Sum
from django.db.models.signals import post_init
from random import Random

class Person(models.Model):
    """Person is the unit of userhood; someone who might go to lunch
    """ 
    name = models.CharField(max_length=30)
    """ name of the person """
    email = models.EmailField(primary_key=True)
    """ email address of the person """

    def save(self, *args, **kwargs):
        # Make sure to add an entry to PairewiseScore for each person 
        people = Person.objects.all()
        for p_email in list(set(map(lambda x: x.email, people))): # unique
            coperson = Person.objects.get(email=p_email)
            pair = sorted([self, coperson], key=lambda x: x.name)
            score = PairwiseScore(holder=pair[0], partner=pair[1], score=1.0)
            score.save()
        super(Person, self).save(*args, **kwargs) 
    
    def delete(self, *args, **kwargs):
        # do something with the book
        scores = PairwiseScore.objects.filter(Q(holder=self)|Q(partner=self))
        for score in scores:
            score.delete()
        super(Person, self).delete(*args, **kwargs)
    
    def __unicode__(self):
        return '%s' % self.name

class PairwiseScore(models.Model):
    """Score between a pair of Person objects
    
    The score is higher the more recently the pair have had lunch
    """
    
    holder = models.ForeignKey(Person, related_name='holder')
    """ first member in the pair """
    partner = models.ForeignKey(Person, related_name='partner')
    """ other member of the pair """
    score = models.DecimalField(max_digits=16, decimal_places=15)
    """ score between the pair """
        
    def __unicode__(self):
        return 'Score(%s, %s) = %f' % (self.holder.name, self.partner.name, self.score)  

class Month(models.Model):
    """Month is the frequency unit for a lunch

    Members participate on a per-month basis
    """

    MONTH_CHOICES = ((1, "January"), (2,"February"), (3, "March"), (4, "April"), (5, "May"), (6, "June"), 
                    (7, "July"), (8, "August"), (9, "September"), (10, "October"), (11, "November"), (12, "December"))
    """ possible months """
    YEAR_CHOICES = tuple(zip(range(2014, 2030), range(2014, 2030))) 
    """ possible years """
    year = models.IntegerField(choices=YEAR_CHOICES)
    """ year when lunch will happen """
    month = models.IntegerField(choices=MONTH_CHOICES)
    """ month when lunch will happen """
    signed_up = models.ManyToManyField(Person, related_name='signed_up', blank=True)
    """ List of Person objects which are signed up for the Month """

    def add_person(self, person):
        """ sign someone up """
        self.signed_up.add(person)

    def remove_person(self, person):
        """ unsubscribe someone """
        self.signed_up.remove(person)

    def __unicode__(self):
        return str(self.get_month_display()) + " " + str(self.get_year_display())

    def make_grouping(self, should_seed=42):
        """ Make the best division of the participants into groupings
        Best means highest sum of group scores
        """
        if should_seed:
            local_random = Random(should_seed)
        group_sizes = self.__get_group_sizes(self.signed_up.count())
        partition = [(y,x+y) for (x, y) in zip(group_sizes, 
            [0] + group_sizes[:len(group_sizes)-1])]
        repn = len(group_sizes) * 100
        people = list(self.signed_up.all())
        max_score = 0.0
        best_groups = [people[group[0]:group[1]] for group in partition]
        for rep in xrange(1, repn):
            local_random.shuffle(people) 
            groups = [people[group[0]:group[1]] for group in partition]
            score = self.__get_score(groups)
            if score > max_score:
                max_score = score
                best_groups = groups
        return best_groups
    
    def __get_score(self, groups):
        """Get the score for a list of groups"""
        cost = 0
        scores = [PairwiseScore.objects.filter(Q(holder__email__in=map(lambda x: x.email, group))).filter(Q(partner__email__in=map(lambda x: x.email, group))).aggregate(score=Sum('score'))['score'] for group in groups]
        if scores[0]:
            return sum(scores)
        return 0.0

    def __get_group_sizes(self, num_people):
        """Decide what the group sizes should be"""
        if num_people <= 5:
            return [num_people]
        else:
            div = 0
            while num_people%4 != 0:
                div+=1
                num_people-=3
            return [3]*div + [4]*(num_people/4)
