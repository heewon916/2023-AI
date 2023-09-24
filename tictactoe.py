from itertools import cycle

HM, AI = 'O', 'X'
PLAYERS = cycle((HM, AI))
WIN_LIST = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6))
BREAK = 0
CONTINUE = 1
DOING = 2


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

    # def get_turn(self):
    #     return self.__turn
    #
    # def set_turn(self, turn):
    #     if turn in (HM, AI):
    #         self.__turn = turn
    #     else:
    #         raise Exception("잘못된 입력입니다.")
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
            return '비겼습니다.'

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
if __name__ == "__main__":
    ttt = TicTacToe()
    while True:
        ttt.print_board()
        ttt.print_turn()

        rst = ttt.user_turn()

        if rst == BREAK:
            msg = ttt.get_win_message()
            if msg:
                print(msg)
            else:
                print("게임을 종료 합니다.")
            break
        elif rst == CONTINUE:
            print("\n[!] 잘못 입력하였습니다. 다시 입력해 주세요.\n")
