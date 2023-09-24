from itertools import cycle

HM, AI = 'O', 'X'
PLAYERS = cycle((HM, AI))
WIN_LIST = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6))
BREAK = 0
CONTINUE = 1
DOING = 2

MODE = ('VS_HM', 'VS_AI')
SCORES = {AI: 1, HM: -1, 'TIE': 0}

class TicTacToe:
    def __init__(self):
        self.__turn = next(PLAYERS)
        self.__winner = ''
        self.__board = ['_'] * 9

    def print_board(self):
        b = self.__board
        print()
        for i in range(0, 9, 3):
            print(f'{b[i]} {b[i + 1]} {b[i + 2]}')

    def print_turn(self):
        print(f'>> {self.__turn} << 차례 입니다.')

    @property
    def turn(self):
        return self.__turn

    @turn.setter
    def turn(self, turn):
        if turn in (HM, AI):
            self.__turn = turn
        else:
            raise Exception("잘못된 입력입니다.")

    @property
    def board(self):
        return self.__board

    # 게임판에 입력하기
    def mark_cell(self, cell):
        if cell == -1 or self.__winner != '':
            return BREAK

        if self.__board[cell] == '_':
            self.__board[cell] = self.__turn
            winner = self.check_board(self.__board[:])

            if winner:
                self.print_board()
                self.__winner = winner
                return BREAK

            self.change_turn()
            return DOING
        else:
            return CONTINUE

    def change_turn(self):
        self.__turn = next(PLAYERS)

    def check_board(self, b):
        winner = ''
        for (x, y, z) in WIN_LIST:
            if b[x] != '_':
                if b[x] == b[y] == b[z]:
                    winner = b[x]
                    return winner

        if '_' in b:
            return ''

        return 'TIE'

    def get_win_message(self):
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
            return self.mark_cell(ans - 1)

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
        board = self.board[:]
        spot, _ = self.__best_choice(AI, board)
        return self.mark_cell(spot)

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
        AI가 이길 때 => MAX 전략 => 1
        사용자 이길 때 => MIN 전략 => -1
        비길 때 => 0
        :param turn:
        :param board:
        :return:
        '''
        winner = self.check_board(board)

        if winner:
            return SCORES[winner]

        # 턴 다음으로 넘기고 다시 best_choice() 호출
        next_turn = HM if turn == AI else AI
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
        ttt.print_board()
        ttt.print_turn()

        if ttt.is_AI_turn():
            rst = ttt.ai_turn()
        else:
            rst = ttt.user_turn()

        if rst == BREAK:
            msg = ttt.get_win_message()
            if msg:
                print(msg)
            else:
                print("게임을 종료 합니다.")
            break
        elif rst == CONTINUE:
            print("잘못 입력하였습니다. 다시 입력해 주세요")
