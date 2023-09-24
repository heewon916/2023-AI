from wikidoc import *
import random

MODE = ('VS_HM', 'VS_AI')
SCORES = {AI: 1, HM: -1, 'TIE': 0}


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
    # def ai_turn(self):
    #     '''
    #     AI가 둘 수 있는 빈칸을 모두 확인하고,
    #     입력할 빈칸을 정하여,
    #     아무 의미 없이 빈칸 중에 랜덤하게 하나의 수를 고르는 것
    #     :return: self.mark_cell(spot)
    #     '''
    #     # AI가 둘 수 있는 빈칸 모두 확인
    #     empty_spots = tuple(i for i, cell in enumerate(self.board) if cell == '_')
    #     if not empty_spots:
    #         return BREAK
    #
    #     # random.choice -> 추후 미니맥스 알고리즘으로 변경 예정
    #     spot = random.choice(empty_spots) # Ai가 입력할 빈칸 정하는 것
    #     return self.mark_cell(spot)
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
