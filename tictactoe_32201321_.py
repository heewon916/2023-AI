from itertools import cycle
import random

HUMAN, AI = 'X', 'O'
PLAYERS = cycle((HUMAN, AI))
WIN_LIST = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6))
BREAK = 0
CONTINUE = 1
DOING = 2

MODE = ('VS_HUMAN', 'VS_AI')
SCORES = {AI: 1, HUMAN: -1, 'TIE': 0}

class TicTacToe:
    def __init__(self):
        self.__turn = next(PLAYERS)     # 현재 차례가 누구인지
        self.__winner = ''              # 승자를 저장
        self.__game_board = ['_'] * 9   # 게임 보드판 정보

    def print_game_board(self):
        c = self.__game_board
        print()
        for i in range(0, 9, 3):
            print(f'{c[i]} {c[i + 1]} {c[i + 2]}')

    def print_turn(self):
        print(f'>> {self.__turn} << 차례 입니다.')

    @property
    def turn(self):
        return self.__turn

    @turn.setter
    def turn(self, turn):
        if turn in (HUMAN, AI):
            self.__turn = turn
        else:
            raise Exception("잘못된 입력입니다.")

    @property
    def board(self):
        return self.__game_board

    # 게임판에 입력하기
    def markOnCell(self, cell):
        '''
        1. 빈칸에만 입력할 것
        2. 입력이 끝나면 승리 체크
        3. 승자 없으면 턴 넘기고
        4. 승자 있으면 승자 출력 후 게임 종료
        :param cell: 1-9 중 입력 -> cell 0-8에 순서대로 매칭
        :return: DOING(계속 진행), CONTINUE(입력 다시 받음), BREAK(승자 존재->게임 종료)
        '''
        if cell == -1 or self.__winner != '':
            return BREAK

        if self.__game_board[cell] == '_':
            self.__game_board[cell] = self.__turn   # 해당 cell 위치에 마크
            winner = self.check_game_board(self.__game_board[:])    # 승자 체크

            # 승자가 있는 경우 => 게임 종료
            if winner:
                self.print_game_board()
                self.__winner = winner
                return BREAK

            # 승자 없는 경우 => 다음 차례로 넘기고
            self.change_turn()
            return DOING
        else:   # 번호 잘못 입력한 경우 => 다시 입력 받기
            return CONTINUE

    def change_turn(self):
        self.__turn = next(PLAYERS)

    def check_game_board(self, b):
        '''
        WIN_LIST를 가지고 승리를 체크함
        b랑 WIN_LIST의 값3개랑 비교해서 모두 같으면 승자 리턴함
        :param b: board의 현재 상태
        :return:
        '''
        winner = ''
        for (x, y, z) in WIN_LIST:
            if b[x] != '_':
                if b[x] == b[y] == b[z]:
                    winner = b[x]
                    return winner

        if '_' in b:
            # 모든 리스트 다 비교했는데 빈칸 남은 경우 => 승자 아직 없음
            return ''

        return 'TIE'

    def get_winner_message(self):
        if self.__winner == '':
            return ''

        if self.__winner == 'TIE':
            return 'X의 승리입니다.(비긴 경우)'

        return f'{self.__winner}의 승리 입니다.'

    def user_turn(self):
        try:
            ans = int(input(">>숫자를 입력하세요(1 ~ 9) [0 : 게임 종료] : "))
        except:
            return CONTINUE

        if ans < 10:
            return self.markOnCell(ans - 1)

        return CONTINUE


#### 게임의 흐름
# 보드를 보여주고 사용자의 입력을 기다린다.
# 사용자가 입력하면 승, 패 여부를 확인한다.
# 승, 패 없을 시 사용자를 변경하고 처음으로 돌아간다
# 승리시 사용자의 승리 메시지 출력하고 종료
# 비길 시 비겼다는 메시지를 출력하고 종료
class TicTacToe_AI(TicTacToe):
    def __init__(self, mode=0):
        super().__init__()
        self.__mode = MODE[mode]

    def is_AI_turn(self):
        '''
        현재의 턴이 AI인지, 사용자인지 확인; 2인용 대전, Ai대전
        mode = 'VS_AI'이면서 turn='AI'일때만 ==> AI 대전
        :return boolean
        '''
        if self.__mode == 'VS_AI' and self.turn == AI:
            return True
        return False

    # AI 대전이 맞을 경우 진행하는 코드
    def ai_turn(self):
        '''
        전체 보드판에 대해서, best_choice() 함수 호출 후
        결정한 해당 spot에 해당 turn에 맞는 표시 기록.
        :return:
        '''
        board = self.board[:]
        spot, _ = self.__best_choice(AI, board)
        return self.markOnCell(spot)

    def __best_choice(self, turn, board):
        '''
        모든 빈칸을 확인하고,
        i번째 c가 빈칸이면, 그 칸을 현재의 turn인 사람의 표시로 칠하고 점수 확인
        점수 가져오는 get_score() = 미니맥스 알고리즘
        점수 가져오기 전에 다시 빈칸으로 만들고
        현재의 점수와 최고 점수를 비교해서
        사용자 턴에는 제일 낮은 점수 MIN, AI턴에는 제일 높은 점수 MAX 리턴
        :param turn:
        :param board:
        :return:
        '''

        # AI인 경우 MAX Player => -10으로 초기화
        # HUMAN인 경우 MIN Player => 10으로 초기화
        bestScore = -10 if turn == AI else 10

        for i, c in enumerate(board):
            if c == '_':
                board[i] = turn
                score = self.__get_score(turn, board)
                board[i] = '_'
                if turn == AI:
                    if bestScore < score:
                        bestScore = score
                        spot = i
                else:
                    if score < bestScore:
                        bestScore = score
                        spot = i
        return spot, bestScore

    def __get_score(self, turn, board):
        '''
        AI가 이길 때 => MAX Player => 1
        사용자 이길 때 => MIN Player => -1
        비길 때 => 0
        :param turn:
        :param board:
        :return:
        '''
        # 1. 승자 먼저 체크
        winner = self.check_game_board(board)
        # 1-1. 승자가 있으면 리턴
        if winner:
            return SCORES[winner]

        # 2. 턴 다음으로 넘기고 다시 best_choice() 호출
        next_turn = HUMAN if turn == AI else AI
        _, bestScore = self.__best_choice(next_turn, board)

        return bestScore


# mode = 0 -> 기존의 2인용
# mode = 1 -> AI 대전
if __name__ == '__main__':
    mode = 0
    try:
        mode = int(input("AI 대전은 1을 입력하세요.(2인용은 엔터 입력)"))
    except:
        pass

    ttt = TicTacToe_AI(mode)
    while True:
        ttt.print_game_board()
        ttt.print_turn()

        if ttt.is_AI_turn():
            rst = ttt.ai_turn()
        else:
            rst = ttt.user_turn()

        if rst == BREAK:
            msg = ttt.get_winner_message()
            if msg:
                print(msg)
            else:
                print("게임을 종료 합니다.")
            break
        elif rst == CONTINUE:
            print("잘못 입력하였습니다. 다시 입력해 주세요")
