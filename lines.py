#!/usr/bin/env python
import random, types
import Tkinter as tk
from functools import partial
'''
# List the defined functions
print "moves_list_special(total,max_adj)"
print "moves_list(board,max_adj)"
print "explicit_partition(board)"
print "moves_to_board"
print "take_turn(move_taken,moves)"
print "list_games(moves_list)"
print "give_partition(moves_list)"
print "poss_partitions_special(total_adj_lines,crossed_lines)"
print "poss_partitions(partition,max_adj_lines)"
print "win_or_lose(partition,max_adj)"
print "winning_sub_parts(partition,max_adj)"
print "losing_sub_parts(partition,max_adj)"
print "part2board(partition,total)"
print "jumble(partition)"
'''
  # PROVED RESULT: p a partition, then p union {I} is a winner if and only if p union {IIII} is a winner
  # Therefore we can always repalce the 4s in a partition with ones
  
  # PROVED RESULT: p a partition, then p is a winner if and only if p union {I X I} is a winner
  # Therefore we can assume a partition has either 1 or 0 single 1s.


  
  
# Right.  Let's try to have 'line game' objects!!  I want to be able to instantiate a game and then take moves until the game is won!
# It should have all the above functions as methods, I guess.
# It should also have the following attributes (that are of course updated every time a move is made):

# max_adj - the maximum number of lines you can cross off in one go.  (Defined at class instantiation.)
# move_history - a list of the moves made so far
# moves_list - a list of the currently available moves
# 



class lines:   # class(partition,max_adj)
  def __init__(self,partition,max_adj):
    # I think it's best to have as few attributes as possible and use methods to calculate what's asked for
    # based on these values when possible.
    self.max_adj = max_adj
    self.top_line = sum(partition) + len(partition) - 1
    self.moves_history = []
    self.board = self.part2board(partition)
    return
  
  def game_current_moves(self):
    # Uses max_adj and board to give current moves list
    return self.moves_list(self.board,self.max_adj)

  def game_take_turn(self,move_taken):
    moves = self.moves_list(self.board,self.max_adj)
    if move_taken not in moves: return -1
    self.moves_history.append(move_taken)
    self.board = self.moves_to_board(self.take_turn(move_taken,moves))
    return
    
  def game_list_games(self):
    moves = self.moves_list(self.board,self.max_adj)
    #if moves == [] : return []
    return self.list_games(moves)
  
  def game_win_or_lose(self):
    current_partition = self.give_partition(self.game_current_moves())
    return self.win_or_lose(current_partition,self.max_adj)
  
  def game_partition(self):
    return self.give_partition(self.game_current_moves())
  
  def game_whos_turn(self):
    if len(self.moves_history) % 2 == 0: return 1  # Player 1's turn
    else: return 2 # Player 2's turn
  
  def game_losing_moves(self):
    winning_sub_partitions = self.winning_sub_parts(self.game_partition(),self.max_adj)
    current_moves = self.game_current_moves()
    losing_moves = []
    for move in current_moves:
      if self.give_partition(self.take_turn(move, current_moves)) in winning_sub_partitions:
        losing_moves.append(move)
    return losing_moves
    
  def game_winning_moves(self):
    winning_moves = [ move for move in self.game_current_moves() if move not in self.game_losing_moves() ]
    return winning_moves
  
  def game_make_winning_move(self):
    winning_moves = self.game_winning_moves()
    if len(winning_moves) != 0:
      random.shuffle(winning_moves)  #  This is so that we make a random winning move
      self.game_take_turn(winning_moves[0])
    else: return -1
  
  def game_make_losing_move(self):
    losing_moves = self.game_losing_moves()
    if len(losing_moves) != 0:
      random.shuffle(losing_moves)  #  This is so that we make a random winning move
      self.game_take_turn(losing_moves[0])
    else: return -1
  
  def game_make_move(self):
    if len(self.game_current_moves()) == 0: return -1
    if self.game_make_winning_move() == -1: self.game_make_losing_move()
    return
  
  def game_board_display(self):
    lines_crossed_off = [ line for move in self.moves_history for line in move ]
    total_lines = sorted(lines_crossed_off + self.board)
    graphic = []
    for i in total_lines:
      if i in self.board: graphic.append(' I ')
      else: graphic.append(' X ')
    return graphic
  
  ################# Private functions ################################################
  def moves_list_special(self,total,max):
    # total : total number of lines in the game
    # max : maximum number of adjacent lines that can be crossed off in a go
    moves = []
    # Need to iterate over number of adjacent lines and line number
    for num_adj_lines in range(1,max + 1):
      for line_num in range(1,total+1):
        if line_num + num_adj_lines -1 <= total:
          # Add the tuple (line_num, .. , line_num + num_adj_lines - 1) to the list 'moves'
          # First create it as a list and then use the 'tuple' function to convert it
          move = []
          for num in range(line_num, line_num + num_adj_lines):
            move.append(num)
          moves.append(move)
          
    return moves

  def explicit_partition(self,board):
    # To be able to generate a moves_list from any game position, I will use the moves_list_special function in a 
    # loop.  Essentially, I'll treat each little set of adjacent lines as 'total', but I need to know where these
    # sets of lines are in the board, so I need a way of getting an explicit partition from any current board set up.
    
    # Get a list of the adj_line lengths and their starting line number.  eg. if board is [2,4,6,7,8], explicit partition is [(2,1),(4,1),(6,3)]
    if board == []: return []
    crossed_lines = [ i for i in range(1,board[-1]) if i not in board ]
    crossed_lines.extend([0,board[-1]+1])  # Add in a crossed line at zero and at the top, then I can just look at the gaps inbetween
    crossed_lines = sorted(crossed_lines)
    explicit_part = []

    for entry in crossed_lines[0:-1]:
      if entry+1 not in crossed_lines: explicit_part.append([entry + 1,crossed_lines[crossed_lines.index(entry)+1]-entry-1])
    return explicit_part  


  def moves_list(self, board, max_adj):
    moves = []
    explicit_part = self.explicit_partition(board)    # Get the explicit partition
    for (start, length) in explicit_part:
      # We now call moves_list_special, remembering that instead of starting at line 1, we're actually starting at line 'start'.
      temp_moves = self.moves_list_special(length, max_adj)
      # Now we need to add (start -1) to every number in temp_moves!
      for i in range(0,len(temp_moves)):
        temp_moves[i] = [(j + start - 1) for j in temp_moves[i]]
      moves.extend(temp_moves)
    return moves

  def moves_to_board(self, moves_list):
    # Given a set of moves, return the board.  This is just all the single length entries in the moves_list
    board = []
    for entry in moves_list:
      if len(entry) == 1: board.append(entry[0])
    return sorted(board)
    
  # Now I need a function that, when given the total list of remaining moves in the game and the move being taken, returns a new list 
  # of the remaining moves
  def take_turn(self, move_taken, moves):
    # Idea is that we go through the elements of 'move_taken' in turn and remove any tuples containing those elements from 'moves'.
    # Have found it's pretty treacherous to have a functionn that edits the arguments it takes (especially when function is used in recursion),
    # so it seems important to make a copy and use that instead of the original
    moves_copy = moves[:]
    for move in moves_copy[:]:  # here I'm iterating over a copy of moves rather than moves itself, as moves itself is being modified by the iteration
      for num in move_taken:
        if num in move: # Remove move from moves
          moves_copy.remove(move)
          break  # No point checking if other elements of move_taken are in 'move' since we've now removed it from the moves list
    
    return moves_copy


  def list_games(self, moves_list):
    # Returns a list of lists, each list is a game
    remaining_moves = moves_list[:]
    if len(remaining_moves) == 1: return [ remaining_moves ]
    if len(remaining_moves) == 0: return -1

    list_of_games = []
    # Here we use recursion.
    # We know that if we only have 1 (or 0) moves in a game, the total list of games is simply that one element.
    # Now imagine we have a list [a, b, c, ..., n] of moves, and that the list [X, Y, Z, ..., Mx] are the remaining moves having taken move 'x'.
    # Since this is a reduced list and finite, we assume we can calculate the total list of games for the remaining moves list, [G1, G2, ..., Gxv]
    # Then the total list of games is [[a]+G1, [a]+G2, ..., [a]+Gav, [b]+G1, [b]+G2, ..., [b]+Gbv, ... [n]+Gnv] - don't quite have the right subscripts
    # here!  But hopefully you can see that, if in a trivial case we can work out a list and in a general case we can reduce it to something simply, we
    # can eventually get there.
    for move in remaining_moves:
      for game in self.list_games(self.take_turn(move,remaining_moves)):
        new_list = [ move ]
        new_list.extend(game)
        list_of_games.append(new_list)
      
    return list_of_games
   
  def give_partition(self, moves_list):
  # Imagine we have two games in the following state (X is a crossed line, I is an uncrossed line)
  # Game 1 is currently:   X X I X I I I X X I X X
  # Game 2 is currently:   I X I X I I I
  # These games are equivalent and can be completely described by their partitions, which I'm defining as a list of lengths of the sets of 
  # adjacent lines, ordered from smallest to largest.  So their partition is [ 1, 1, 3 ]
  # I want a function that will take a moves list and return the partition, so we can easily see if two games are equivalent.
    partition = []
    single_lines = []
    length = 0
    if len(moves_list) == 0: return []
    # First step - make a list of the available single moves
    for move in sorted(moves_list):
      if len(move) == 1: single_lines.append(move[0])
    # Go from the bottom one to the top one computing lengths of the partition bits
    # I actually go from bottom one to top one +1, since I only add in a partition bit when I reach a number that's not in the single_lines list,
    # and the top number might be in!  (It looks like +2 below, but remember range[1,4] gives [1,2,3])  
    for num in range(single_lines[0],single_lines[-1]+2):
      if num in single_lines: length = length + 1
      else:
        # num not in the list of available single lines means we have reached the end of part of the partition (add it) or not yet
        # started one (ie. the previous num hadn't been in the set of single lines either)
        if length != 0:
          partition.append(length)
          length = 0
    return sorted(partition)

  # Should be able to use the partitions idea to have a much more efficient way of calculating possible games.
  # Rather than a list of moves, I could specify a game ('up to symmetry') by a list of partitions
  # The only extra information we need is the maximum number of adjacent lines you're allowed to cross off in one go
  # Will be interesting to find out how many different games there reeeaaally are for a given moves list
  # You guessed it - I now want a function that does that ...

  # First, a function to do a special case - when we're crossing off a fixed number of lines from a fixed set of adjacent lines
  def poss_partitions_special(self, total_adj_lines,crossed_lines):
    # total_adj_lines is just the number of lines
    # crossed_lines is the number of lines we're intending to cross
    if total_adj_lines < crossed_lines:
      return -1  # since you can't cross off more lines than you have
    if total_adj_lines == crossed_lines:
      return []  # There is no partition if you cross off all the lines you have  
    partitions = []
    i = 0
    for i in range(1,total_adj_lines + 1 - crossed_lines):  # Don't have to go all the way along - just need to think what upper limit should be
      j = i + crossed_lines -1  # j is the top line of the set of adjacent lines you're crossing off
      new_partition = [i-1, total_adj_lines - j]
      if 0 in new_partition:
        new_partition.remove(0)
      partitions.append(sorted(new_partition))
    
    # Now we want to ensure the entries are unique, so we sort them and go through the list, checking at each point that the next entry isn't the same
    # If it is, we remove the current entry
    sorted_partitions = sorted(partitions)
    for entry in sorted_partitions[:-2]:   # Rem: don't iterate over something you're modifying, and no point looking at the last
                                           # entry as there's nothing after it that it might be a duplicate of
      if sorted_partitions[sorted_partitions.index(entry) + 1] == entry:
        sorted_partitions.remove(entry)  # remove duplicated entries from partitions
    return sorted_partitions

  # In the function below, I want to add a hash table functionality
  poss_partitions_hash={}
  def poss_partitions(self, partition,max_adj_lines):
    poss_partitions_hash = self.poss_partitions_hash
    if tuple(sorted(partition)) in poss_partitions_hash: return list(poss_partitions_hash[tuple(sorted(partition))])
    # ok, given a partition, what are the possible partitions when we can cross off up to max_adj_lines adjacent lines?
    partitions_list = []
    for adj_lines in range(1, max_adj_lines + 1):
      # Create a new list, entries a subset of partitions, where entries are unique and >= adj_lines
      unique_entries = []
      for entry in sorted(partition):
        if entry >= adj_lines and entry not in unique_entries: unique_entries.append(entry)
      for entry in unique_entries:
        copy = sorted(partition)[:]
        copy.remove(entry)  # Remove the set of adjacent lines we're splitting by crossing some lines in it ...
        if len(self.poss_partitions_special(entry,adj_lines)) > 0:  # remember that if nothing is returned, we haven't split a set of adjacent lines 
                                                               # into two - we've actually crossed the whole set off.
          for element in self.poss_partitions_special(entry,adj_lines):   # each element is a possible new bit of the partition
            new_copy = copy[:]
            new_copy.extend(element)   # now new_copy is our old partition without the set of adjacent lines we split up by crossing
                                       # some off and but with the resulting new bits due to that move
            # Currently I'm missing the cases when poss_partitions_special returns the empty list
            partitions_list.append(sorted(new_copy))
        else:
          partitions_list.append(copy)
    poss_partitions_hash[tuple(sorted(partition))] = sorted(partitions_list)      
    return sorted(partitions_list)

  def poss_partitions_special_v2(self, total_adj_lines,crossed_lines):
    # total_adj_lines is just the number of lines
    # crossed_lines is the number of lines we're intending to cross
    if total_adj_lines < crossed_lines:
      return -1  # since you can't cross off more lines than you have
    if total_adj_lines == crossed_lines:
      return []  # There is no partition if you cross off all the lines you have  
    partitions = []
    i = 0
    for i in range(1,total_adj_lines + 1 - crossed_lines):
      if i > (total_adj_lines + 1)/2 : break # Don't have to go all the way along - just need to think what upper limit should be
      j = i + crossed_lines -1  # j is the top line of the set of adjacent lines you're crossing off
      new_partition = [i-1, total_adj_lines - j]
      if 0 in new_partition:
        new_partition.remove(0)
      remove_4s_and_1_pairs(new_partition)
      partitions.append(sorted(new_partition))
    
    # Now we want to ensure the entries are unique, so we sort them and go through the list, checking at each point that the next entry isn't the same
    # If it is, we remove the current entry
    sorted_partitions = sorted(partitions)
    for entry in sorted_partitions[:-2]:   # Rem: don't iterate over something you're modifying, and no point looking at the last
                                           # entry as there's nothing after it that it might be a duplicate of
      if sorted_partitions[sorted_partitions.index(entry) + 1] == entry:
        sorted_partitions.remove(entry)  # remove duplicated entries from partitions
    return sorted_partitions
    
    
  def remove_4s_and_1_pairs(self, partition):
    while 4 in partition:
      partition.remove(4)
      partition.insert(0,1)  # insert a 1 at the start of the list
    partition = sorted(partition)  # this ensures all the 1s are at the front
    while len(partition) > 1:
      if partition[1] == 1:
        partition = partition[2:]  # chop off the front two entries (which are 1)
      else: break
    return partition
    
  poss_partitions_v2_hash = {}
  def poss_partitions_v2(self, partition,max_adj_lines):
    # Due to the results listed at the top, we can replace 4s with 1s and then get rid of pairs of ones.
      
    reduced_part = partition[:]
    remove_4s_and_1_pairs(reduced_part)
    
    if tuple(reduced_part) in poss_partitions_hash: return list(poss_partitions_v2_hash[tuple(reduced_part)])
    # ok, given a partition, what are the possible partitions when we can cross off up to max_adj_lines adjacent lines?
    partitions_list = []
    for adj_lines in range(1, max_adj_lines + 1):
      # Create a new list, entries a subset of partitions, where entries are unique and >= adj_lines
      unique_entries = []
      for entry in reduced_part:
        if entry >= adj_lines and entry not in unique_entries: unique_entries.append(entry)
      for entry in unique_entries:
        copy = reduced_part[:]
        copy.remove(entry)  # Remove the set of adjacent lines we're splitting by crossing some lines in it ...
        if len(self.poss_partitions_special_v2(entry,adj_lines)) > 0:  # remember that if nothing is returned, we haven't split a set of adjacent lines 
                                                               # into two - we've actually crossed the whole set off.
          for element in self.poss_partitions_special_v2(entry,adj_lines):   # each element is a possible new bit of the partition
            new_copy = copy[:]
            new_copy.extend(element)   # now new_copy is our old partition without the set of adjacent lines we split up by crossing
                                       # some off and but with the resulting new bits due to that move
            
            
            
            partitions_list.append(sorted(remove_4s_and_1_pairs(new_copy)))
        else:
          partitions_list.append(remove_4s_and_1_pairs(copy))
    poss_partitions_v2_hash[tuple(reduced_part)] = sorted(partitions_list)      
    return sorted(partitions_list)
    
  win_or_lose_hash={}
  def win_or_lose(self, partition, max_adj):
    win_or_lose_hash = self.win_or_lose_hash
    # Right guys, this is the daddy.  Given a position, can I win?
    # Like list_games, this is iterative, but we've used the idea of partitions and hopefully a hash table to try and speed it up.
    
    # win_or_lose on any empty partition should be a winning position - if it's your turn and there are no moves left, you've won.
    if len(partition) == 0 : return 1
    
    # First, the special cases:
    if len(partition) == 1 and sorted(partition)[0] <= max_adj + 1:
      if 1 < sorted(partition)[0]:
        return 1  # If you can cross off all but the last line on your go, you've won
      else: return -1  # if there's only one line left, I'm afraid you're forced to cross it off and you've lost
    
    
    # Now the general case:
    for part in self.poss_partitions(sorted(partition), max_adj):
      if tuple(part) not in win_or_lose_hash:
        win_or_lose_hash[tuple(part)] = self.win_or_lose(part, max_adj) # I don't know what the syntax is, but building up a DB of winners / losers should help speed this up a lot
      if win_or_lose_hash[tuple(part)] == -1:
        return 1  # If at least one sub-partition is a loser, this is a winner.
    return -1      # If all sub_partitions are winners, this is a loser.

  win_or_lose_v2_hash = {}
  def win_or_lose_v2(self, partition, max_adj):
    win_or_lose_v2_hash = self.win_or_lose_v2_hash
    # Right guys, this is the daddy.  Given a position, can I win?
    # Like list_games, this is iterative, but we've used the idea of partitions and hopefully a hash table to try and speed it up.
    
    # win_or_lose on any empty partition should be a winning position - if it's your turn and there are no moves left, you've won.
    if len(partition) == 0 : return 1
    
    # First, the special case:
    if len(partition) == 1 and sorted(partition)[0] <= max_adj + 1:
      if 1 < sorted(partition)[0]:
        return 1  # If you can cross off all but the last line on your go, you've won
      else: return -1  # if there's only one line left, I'm afraid you're forced to cross it off and you've lost
    
    # Now the general case:
    for part in self.poss_partitions_v2(sorted(partition), max_adj):
      if tuple(part) not in win_or_lose_v2_hash:
        win_or_lose_v2_hash[tuple(part)] = win_or_lose_v2(part, max_adj) # I don't know what the syntax is, but building up a DB of winners / losers should help speed this up a lot
      if win_or_lose_v2_hash[tuple(part)] == -1:
        return 1  # If at least one sub-partition is a loser, this is a winner.
    return -1      # If all sub_partitions are winners, this is a loser.
    
    
  def winning_sub_parts(self, partition, max_adj):
    list = self.poss_partitions(sorted(partition),max_adj)
    new_list = []
    for entry in list: 
      if self.win_or_lose(entry, max_adj) == 1: new_list.append(entry)
    return new_list

  def losing_sub_parts(self, partition, max_adj):
    list = self.poss_partitions(sorted(partition),max_adj)
    new_list = []
    for entry in list: 
      if self.win_or_lose(entry, max_adj) == -1: new_list.append(entry)
    return new_list

  def part2board(self, partition):
    # A function to show you the current status - which lines have been crossed off
    # Result will be a list of numbers where each number represents a line.  If the number's not there, it's been crossed off.
    # So this will essentially just put an empty space between the partition bits, and then the remaining spaces at the end.
    # It's meant to be the reverse (as much as it can be, because in going one way we lose information) of the 'give_partition' function
    #if total < len(partition) - 1 + sum(partition) : return -1  # We need to be able to separate each element of the partition with a crossed off line 
    board = []
    start_of_adj_lines = 1  # Each time we add a bit of the partition to the board, we remember the place where we start and count on up
    for adj_lines in partition:
      for i in range(0,adj_lines):
        board.append(i + start_of_adj_lines)
      start_of_adj_lines = start_of_adj_lines + adj_lines + 1 # This is the starting position for the next adj_lines after having left a 1 gap
    return board


  def jumble(self, partition):
    # Just a fun function to randomise the entries in a partition - there's no need for them to be in order
    random.shuffle(partition)
    return partition
  
class GUI:

    def __init__(self, master):
      # I want a menu where I can select Level, Number of Lines, Max Adj and Start
      self.frames = {}  # Will have a dictionary of frames
      self.choices = {}
      
      self.frames['Level'] = tk.Frame(master)
      self.frames['Level'].pack(side=tk.LEFT)
      self.frames[('Level','Menu')] = tk.Menubutton(self.frames['Level'],relief=tk.RAISED,borderwidth=1,text='Level')
      self.frames[('Level','Menu')].pack(fill=tk.X,side=tk.TOP)
      menu = self.frames[('Level','Menu')]
      menu.menu = tk.Menu(menu, tearoff=0)
      for entry in ['Easy','Hard','No mistakes ...']:
        menu.menu.add_command(label=entry, command = partial(self.update,entry,menu))
      menu['menu'] = menu.menu  
      menu.choice = tk.StringVar()
      menu.choice.set('Easy')
      entry = tk.Entry(self.frames['Level'],textvariable = menu.choice,state=tk.DISABLED,disabledforeground='black',insertborderwidth=3,width=14)
      entry.pack(fill=tk.X,side=tk.BOTTOM)
      self.choices['Level'] = menu.choice.get

      self.frames['Number of Lines'] = tk.Frame(master)
      self.frames['Number of Lines'].pack(side=tk.LEFT)
      self.frames[('Number of Lines','Menu')] = tk.Menubutton(self.frames['Number of Lines'],relief=tk.RAISED,borderwidth=1,text='Number of Lines')
      self.frames[('Number of Lines','Menu')].pack(fill=tk.X,side=tk.TOP)
      menu = self.frames[('Number of Lines','Menu')]
      menu.menu = tk.Menu(menu, tearoff=0)
      for entry in range(1,11):
        menu.menu.add_command(label=str(entry), command = partial(self.update,entry,menu))
      menu['menu'] = menu.menu  
      menu.choice = tk.StringVar()
      menu.choice.set('7')
      entry = tk.Entry(self.frames['Number of Lines'],textvariable = menu.choice,disabledforeground='black',insertborderwidth=3,width=14)
      entry.pack(fill=tk.X,side=tk.BOTTOM)
      self.choices['Number of Lines'] = menu.choice.get

      self.frames['Max Adj'] = tk.Frame(master)
      self.frames['Max Adj'].pack(side=tk.LEFT)
      self.frames[('Max Adj','Menu')] = tk.Menubutton(self.frames['Max Adj'],relief=tk.RAISED,borderwidth=1,text='Max Adj')
      self.frames[('Max Adj','Menu')].pack(fill=tk.X,side=tk.TOP)
      menu = self.frames[('Max Adj','Menu')]
      menu.menu = tk.Menu(menu, tearoff=0)
      for entry in range(1,5):
        menu.menu.add_command(label=str(entry), command = partial(self.update,entry,menu))
      menu['menu'] = menu.menu  
      menu.choice = tk.StringVar()
      menu.choice.set('2')
      entry = tk.Entry(self.frames['Max Adj'],textvariable = menu.choice,disabledforeground='black',insertborderwidth=3,width=14)
      entry.pack(fill=tk.X,side=tk.BOTTOM)
      self.choices['Max Adj'] = menu.choice.get

      self.frames['Start'] = tk.Frame(master)
      self.frames['Start'].pack(side=tk.LEFT)
      level_choice = self.frames[('Level','Menu')].choice.get
      line_number_choice = self.frames[('Number of Lines','Menu')].choice.get
      max_adj_choice = self.frames[('Max Adj','Menu')].choice.get
      button = tk.Button(self.frames['Start'],text='Start!!', activebackground='green',height = 2,command=partial(self.start,master,level_choice,line_number_choice,max_adj_choice))
      button.pack()

    
    def update(self,entry,menu):
      menu.choice.set(entry)
    
    def start(self,master,level_choice,line_number_choice,max_adj_choice):
      game_root = tk.Tk()
      game_root.title('Lines!!')
      game = lines([int(line_number_choice())],int(max_adj_choice()))
      GAME(game_root,game)
      game_root.mainloop()
      return
      
class GAME:

  # Colour scheme!  The way I've made it, the buttons must have different colours for their 3 different states
  colours = dict([('unpressed','#EEE8CD'),('initial_press','#FFD700'),('confirmed_press','#000000')])
  buttons = {}
  other_buttons = {}
  # Not efficient, I guess, but I'm becoming paranoid about keeping my options open, so I prefer to set up
  # a dict even if it's not clear I'll need one.
  menu_options = dict([('Suggest winning move',''),(2,''),(3,'')])
  def __init__(self, master, game):
    # Defining the colour scheme!
    game_frame = tk.Frame(master)
    game_frame.pack()
    self.game_frame = game_frame
    button_frame = tk.Frame(game_frame)
    button_frame.pack(side=tk.TOP)
    for number in range(1,game.top_line+1):
      # I am making a dictionary of dictionaries.  Each entry in 'buttons' is a dictionary containing the button variables.
      # self.buttons keys are the numbers of the lines.
      # Each individual line dictionary has: 'button - the button reference, 'colour' - the colour StringVar, 'pressed' - Boolean
      self.buttons[number] = {}
      button_dict = self.buttons[number]
      # Add the colour of the button
      colour = tk.StringVar()
      colour.set(self.colours['unpressed'])
      button_dict['colour'] = colour
      # Add the button reference itself (and pack it)
      button_dict['button'] = tk.Button(button_frame,height=5,width=5,text=number)
      button_dict['button'].pack(side=tk.LEFT)
      button_dict['button'].configure(bg=colour.get(),command = partial(self.cross_line,button_dict))
    other_buttons_frame = tk.Frame(game_frame)
    other_buttons_frame.pack(side=tk.TOP)

    # Add the button to press when you make your own move
    self.other_buttons['commit'] = {}
    self.other_buttons['commit']['button'] = tk.Button(other_buttons_frame,height=1,text='Make my move',command = partial(self.take_turn,game))
    self.other_buttons['commit']['button'].pack(side=tk.LEFT)
    # Add a small menu button
    self.other_buttons['?'] = {}
    self.other_buttons['?']['button'] = tk.Menubutton(other_buttons_frame,relief=tk.RAISED,borderwidth=1,text='?')
    self.other_buttons['?']['button'].pack(side=tk.LEFT)
    self.other_buttons['?']['options'] = tk.Menu(self.other_buttons['?']['button'], tearoff=0)
    for entry in self.menu_options.keys():
      self.other_buttons['?']['options'].add_command(label=entry, command = partial(self.menu_choice,entry,game))
    # Associate options with the menu
    self.other_buttons['?']['button']['menu'] = self.other_buttons['?']['options']
    
    # Add a button to ask the computer to take a go
    self.other_buttons['computer_turn'] = {}
    self.other_buttons['computer_turn']['button'] = tk.Button(other_buttons_frame,height=1,text='Computer move',command = partial(self.computer_turn,game))
    self.other_buttons['computer_turn']['button'].pack(side=tk.RIGHT)
  
  def menu_choice(self,entry,game):
    print "You chose %s" % entry
    if entry == 'Suggest winning move':
      # Clear any partially pressed buttons
      self.clear_initial_presses()
      winning_moves = game.game_winning_moves()
      random.shuffle(winning_moves)
      if len(winning_moves) != 0:
        winning_move = winning_moves[0]
        for button_number in winning_move:
          button_dict = self.buttons[button_number]
          self.cross_line(button_dict)
      else:
        print "No winning moves available"
    return
  
  def cross_line(self,button_dict):
    colour = button_dict['colour']
    button = button_dict['button']
    if colour.get() == self.colours['initial_press']: colour.set(self.colours['unpressed'])
    else: colour.set(self.colours['initial_press'])
    button.configure(bg=colour.get())
  
  def clear_initial_presses(self):
    #  If you choose some kind of option (take computer turn, for example) when you're midway
    # through a go and have tentatively pressed a few buttons, this function unpresses them.
    pressed_buttons = [ number for number in self.buttons.keys() if self.buttons[number]['colour'].get() == self.colours['initial_press'] ]
    for number in pressed_buttons:
      colour = self.buttons[number]['colour']
      colour.set(self.colours['unpressed'])
      button = self.buttons[number]['button']
      button.configure(bg=colour.get())
    return

  def computer_turn(self,game):
    self.clear_initial_presses()
    exit_code = game.game_make_move()  # This calls the function to take the move and sets the exit code
    if exit_code != -1:  # ie. If there was a move to be made and the game hasn't already ended ...
      move_made = game.moves_history[-1]
      self.other_buttons['commit']['button'].configure(relief=tk.RAISED)
      self.other_buttons['computer_turn']['button'].configure(relief=tk.SUNKEN)
      for number in move_made:
        colour = self.buttons[number]['colour']
        colour.set(self.colours['confirmed_press'])
        self.buttons[number]['button'].configure(bg=colour.get(),state=tk.DISABLED)
    self.has_game_finished(game,'computer')
    return
    
  def take_turn(self,game):
    # Make a list of all the pressed buttons
    # if that list is in game.currents_moves(), commit to the presses.
    pressed_buttons = [ number for number in self.buttons.keys() if self.buttons[number]['colour'].get() == self.colours['initial_press'] ]
    if pressed_buttons in game.game_current_moves():
      game.game_take_turn(pressed_buttons)   # This take the turn in the actual game object
      self.other_buttons['commit']['button'].configure(relief=tk.SUNKEN)
      self.other_buttons['computer_turn']['button'].configure(relief=tk.RAISED)
      for number in pressed_buttons:
        colour = self.buttons[number]['colour']
        colour.set(self.colours['confirmed_press'])
        self.buttons[number]['button'].configure(bg=colour.get(),state=tk.DISABLED)
    self.has_game_finished(game,'player')
    return
   
  def has_game_finished(self,game,loser):
    if len(game.game_current_moves()) == 0:
      # Game has been lost by loser
      # Wish to make all the buttons flash randomly and for 'You won!' or 'I won!' to appear as appropriate
      
      # First, disable the take turn buttons
      self.other_buttons['commit']['button'].configure(state=tk.DISABLED)
      self.other_buttons['computer_turn']['button'].configure(state=tk.DISABLED)
      
      # Now shuffle a list of the lines
      line_order = [ line for line in range(1,game.top_line+1) ]
      random.shuffle(line_order)
      
      # Now, in this shuffled order, make each button flash,assign a random colour and the appropriate text character.
      # Note I also have to force an update of the game_frame here, else the colours would only update when
      # this function finishes and Tkinter gets back to its main loop.
      
      # Calculating appropriate text characters ...
      if loser == 'computer': text = 'You win'
      else: text = 'I win'
      message = {}
      if len(text) <= len(range(game.top_line)):  # Make sure there's actually enough buttons for the message
        text = text.center(game.top_line)         # pad the message with spaces on the outside
        for i in range(1,game.top_line+1):
          message[i] = text[i-1]                  # Want line number 1 to hold first character of message - that is, text[0] ...
      else: 
        for i in range(1,game.top_line+1):
          message[i] = ''                         # If there's not enough space for the message, don't have one.
      for line in line_order:
        self.game_frame.update()
        # Make line flash and assign a random colour - button has to be active to flash!
        self.buttons[line]['button'].configure(state=tk.ACTIVE)
        self.buttons[line]['button'].flash()
        rcolour = '#' + "".join(["%02x" % random.randrange(256) for i in range(3)])  # Saw this line on the net!  'x' seems to convert to HEX
        self.buttons[line]['button'].configure(state=tk.DISABLED,text=message[line],bg=rcolour)
    return
   
def main():
    root = tk.Tk()
    root.title('Lines Menu')
    GUI(root)
    root.mainloop()
    return

if __name__ == "__main__":
    main()


