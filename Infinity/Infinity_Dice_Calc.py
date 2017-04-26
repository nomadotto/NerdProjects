# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 09:54:38 2017

@author: nedd
"""
import pandas
import matplotlib.pyplot as plt



##INFINITY ODDS CALCULATORS:

class Infinity_Calc():
    @staticmethod
    def Expected_Number_of_Successes(skill, ndice, focus = 1):
        prob_two_success = focus/20.0
        prob_one_success = (skill-focus)/20.0
        
        nsuccess = 2*prob_two_success*ndice
        nsuccess += prob_one_success*ndice
        
        return nsuccess
    
    @staticmethod
    def Prob_Success(skill, ndice, difficulty, focus =1):
        total_outcomes = 20.0**ndice
        n_hits = 0.0
        n_misses = 0.0
        for i in range(int(total_outcomes)):
            dice = Infinity_Calc.Parse_Outcome(i, ndice)
            nsucc = Infinity_Calc.Calc_Successes(dice, skill, focus)
            if nsucc >= difficulty:
                n_hits+=1
            else:
                n_misses +=1
    
        try:            
            assert n_hits + n_misses == total_outcomes
        except AssertionError:
            print("Outcomes were Dropped")
        return n_hits/total_outcomes
                
    @staticmethod
    def Make_Success_Matrix(focus = 1):
        df = pandas.DataFrame()
        for skill in range(1,20):
            results= []
            for ndice in range(1,6):
                results.append(Infinity_Calc.Expected_Number_of_Successes(skill, ndice, focus))
            df[skill] = results
        return df
        
                
    @staticmethod
    def Calc_Successes(iterable, skill, focus):
        nsuccess = 0
        for elem in iterable:
            if elem <= focus:
                nsuccess+=2
            elif elem <= skill:
                nsuccess+=1
            else:
                nsuccess +=0
        return nsuccess
            
        
    @staticmethod
    def Parse_Outcome(outcomenum, ndice):
        quo = outcomenum
        dice = [1 for i in range(ndice)]
        n = 0
        while quo >0:
            quo,rem = divmod(quo,20)
            dice[n] +=rem
            n+=1
        return dice
        
        
    @staticmethod
    def Make_Single_Success_Curve(skill, difficulty, focus=1):
        prob_success = []
        for ndice in range(1,6):
            prob_success.append(Infinity_Calc.Prob_Success(skill, ndice, difficulty, focus =1))
        plt.plot(range(1,6), prob_success)
        plt.xlabel('Number of Dice')
        plt.ylabel('Success Probability')
        plt.title('Probability Distribution for %s skill, %s difficulty, %s focus' %(str(skill), str(difficulty), str(focus)))
        plt.show()
             
             
             
    @staticmethod
    def Make_Dice_Advantage_Curve(ndice, difficulty, focus =1):
        succ_per_diff = []
        skills = []
        for skill in range(focus+1,20):
            ndice_succ = Infinity_Calc.Prob_Success(skill, ndice, difficulty, focus)
            ndice_1_succ = Infinity_Calc.Prob_Success(skill, ndice+1, difficulty, focus)
            succ_per_diff.append(ndice_1_succ - ndice_succ)
            skills.append(skill)
        plt.plot(skills, succ_per_diff)
        plt.xlabel('Skill')
        plt.ylabel('% Point Increase from adding an extra die')
        plt.title('Gain in Probability of Success going from %s to %s dice on a difficulty %s test' % (str(ndice), str(ndice +1), str(difficulty) ))
        plt.show()
             
    @staticmethod
    def Calc_Opposed_Probability(myskill, yourskill, mydice, yourdice =1):
        total_my_outcomes = 20.0**mydice
        total_your_outcomes = 20.0**yourdice
        n_all_outcomes = total_my_outcomes*total_your_outcomes
        n_my_hits = 0.0
        n_i_win =0
        n_you_win = 0
        n_your_hits =0.0
        n_both_misses = 0.0
        counter = 0
        for i in range(int(total_my_outcomes)):
            for j in range(int(total_your_outcomes)):
                counter +=1
                if counter%int(.1*n_all_outcomes) ==0:
                    print str(counter / int(.1*n_all_outcomes)) + "0 percent done "
                active_dice =  Infinity_Calc.Parse_Outcome(i, mydice)
                reactive_dice = Infinity_Calc.Parse_Outcome(j, yourdice)
                maxactive =0
                maxreactive = 0
                for die in active_dice:
                    if die > maxactive and die <= myskill:
                        maxactive = die
                for die in reactive_dice:
                    if die > maxreactive and die <= yourskill:
                        maxreactive = die
                i_hit = False
                you_hit = False
                for active_die in active_dice:
                    if (active_die > maxreactive) & (active_die <= myskill):
                        n_my_hits +=1
                        i_hit = True
                for reactive_die in reactive_dice:
                    if (reactive_die > maxactive) & (reactive_die <= yourskill):
                        n_your_hits += 1
                        you_hit= True
                try:
                    assert not(i_hit and you_hit)
                    n_i_win += i_hit
                    n_you_win += you_hit
                    n_both_misses += not(i_hit) and not(you_hit)
                except AssertionError:
                    print "Both can't hit, something is wrong"
                    return
        output = {}
        output['my_hits'] = n_my_hits
        output['your_hits'] = n_your_hits
        output['my_wins'] = n_i_win
        output['your_wins'] = n_you_win
        output['both_miss'] = n_both_misses
        output['my_hit_prob'] = n_i_win/(n_i_win+ n_you_win + n_both_misses)
        output['your_hit_prob']=  n_you_win/(n_i_win + n_you_win + n_both_misses)
        return output
        
    @staticmethod
    def Make_Opposed_Skill_Curve(your_skill, my_dice, your_dice = 1):
        my_curve = []
        my_skill = range(1,20)
        your_curve = []
        for skill in my_skill:
            output = Infinity_Calc.Calc_Opposed_Probability(skill, your_skill, my_dice, your_dice)
            my_curve.append(output['my_hit_prob'])
            your_curve.append(output['your_hit_prob'])
        plt.plot(my_skill, my_curve, 'b-', label = 'my_success_curve')
        plt.plot(my_skill, your_curve, 'r.', label = 'your_success_curve')
        plt.xlabel('My Skill')
        plt.ylabel('Odds of Success')
        plt.title('Skill Success Curves for FtF Rolls, your skill: %s, my_dice %s, your_dice %s' % (str(your_skill ), str(my_dice), str(your_dice)))
        plt.legend(loc = 2)
        
    
        
            
                    
                    
                