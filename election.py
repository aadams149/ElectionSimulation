#!/usr/bin/env python
# coding: utf-8

# In[1]:


import jdc


# In[3]:


class Election:
    
    def __init__(self,candidates,parties,voters,method,polls):
        self._candidates = candidates
        self._parties = parties
        self._voters = voters
        self._method = method
        self._polls = polls
        
    def candidate_names(self):
        return self._candidates
    
    def party_names(self):
        return self._parties
    
    def voter_count(self):
        return self._voters
    
    def election_type(self):
        return self._method


# In[4]:

    def Ballots(self,
                candidates,
                polls,
                electorate,
                method):
            candidates.append('N/A')
            if method == 'FPTP':
                num_choices = 1
            if method == 'RCV':
                num_choices = len(candidates)
            if method == 'Approval':
                num_choices = lambda: random.randint(1,len(candidates))
        
            ballots = []
            for k in electorate:
                ballots_cast = [np.random.choice(candidates,
                                                size = num_choices,
                                                replace = False,
                                                p=polls) for _ in range(electorate[k])]
                ballots_cast = pd.DataFrame(ballots_cast)
                ballots_cast['demographic'] = k
                ballots.append(ballots_cast)
        
            ballots = pd.concat(ballots)
            return(ballots)
    
    def fix_NAs(ballots):
            for ballot in ballots:
                for i,cand in enumerate(ballot):
                    if ballot[i-1] == 'N/A':
                        ballot[i] = 'N/A'
            return(ballots)

    def FPTPVoting(self,
               candidates,
               polls,
               electorate):
        votes = Ballots(method = 'FPTP',
                       candidates = candidates,
                       polls = polls,
                       electorate = electorate)
        votes = pd.DataFrame(votes)
        votes = pd.DataFrame(ballots.
                             value_counts().
                             rename_axis('candidates').
                             reset_index(name = 'raw_votes'))
        votes['percentage'] = votes['votes']/sum(votes['votes'])
        self._winner = votes.loc[votes['votes'].idxmax()]['candidates']
        
        if self._winner == 'N/A':
            self._winner = votes.nlargest(2,'votes')['candidates'][1]

    def RankedChoiceVoting(self,
                       candidates,
                       polls,
                       voters,
                       full_eval = True,
                       return_ballots = False):
        votes = Ballots(method = 'RCV',
                       candidates = candidates,
                       polls = polls,
                       voters = voters)
        votes = fix_NAs(votes)
        votes = pd.DataFrame(votes)
        column_names = []
        for j in range(1,len(votes.columns)):
            name = "round_"+str(j)
            column_names.append(name)
        votes.columns = column_names
        totals = pd.DataFrame(votes.value_counts(['round_1'])).rename_axis('candidates').reset_index(name = 'round_1_votes')
        totals['percentage'] = totals['round_1_votes']/sum(totals['round_1_votes'])
        vote_round = 1
        
        for m in range(1,len(votes.columns)):
            if full_eval == False:
                if any(totals['percentage'] >= 0.5):
                    self._winner = totals.loc[totals['percentage'].idxmax()]['candidates']
                    break
            str_prev = 'round'+str(vote_round)
            elim_cand = totals.loc[totals['percentage'].idxmin()]['candidates']
            next_round = votes[votes[str_prev] == elim_cand]
            vote_round = vote_round+1
            str_current = 'round'+str(vote_round)
            next_round = pd.DataFrame(
                next_round.value_counts(
                    [str_current])).rename_axis('candidates').reset_index(name = str_current+'_votes')
            totals = totals.merge(next_round,
                                 how = 'left',
                                 on = 'candidates')
            totals[str_current+'votes'] = totals[str_prev+'votes'] + totals[str_current+'votes']
            totals['percentage'] = totals[str_current+'votes']/sum(totals[str_current+'votes'])
            if vote_round == len(votes.columns):
                break
        
        if return_ballots == True:
            output = []
            output.append(votes)
            output.append(totals)
            return(output)
        else:
            return(totals)

