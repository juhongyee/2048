#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
#include <random>
using namespace std;
#define BOARD_SIZE 5
// !!! 해당 방향으로 못 움직일 때 에러

// 2048 게임 구현
vector<vector<int>> board(BOARD_SIZE, vector<int>(BOARD_SIZE, 0));

int random_create();           // 빈 칸에 랜덤으로 2 또는 4 생성
void create(int num);              // 빈 칸에 특정 숫자 생성
void write_line();             // 게임 보드 구분선 출력
void print_board(string input, int score); // 게임 보드 출력
bool is_full();                // 보드가 가득찼는지 확인

void up();    // 위로 밀기
void down();  // 아래로 밀기
void left();  // 왼쪽으로 밀기
void right(); // 오른쪽으로 밀기

int main()
{
    int score = 0;
    score += random_create(); // -1이면 게임 종료지만 가능성 없으니 구현 안함
    score += random_create();
    print_board("게임 시작! 2048을 만들어보세요!", score);

    while (true)
    {
        // 게임 시작 시 랜덤한 곳에 4 하나 2 하나 생성

        string input;
        cout << "up: 위로, down: 아래로, left: 왼쪽으로, right: 오른쪽으로\nexit 또는 그 외: 종료\n움직일 방향을 입력하세요: ";
        cin >> input;

        /** input 값에 따라 up(), down(), left(), right() 함수 호출 */
        if (input.compare("up") == 0)
        {
            up();
        }
        else if (input.compare("down") == 0)
        {
            down();
        }
        else if (input.compare("left") == 0)
        {
            left();
        }
        else if (input.compare("right") == 0)
        {
            right();
        }
        else
        {
            cout << "Game Over! 2048 게임을 종료합니다\n";
            cout << "최종 점수: " << score << "\n";
            break;
        }
        // 옮기기 끝내고 새 블록 추가
        int i = random_create();
        if (i == -1)
        {
            cout << "Game Over! 2048 게임을 종료합니다\n";
            cout << "최종 점수: " << score << "\n";
            break;
        }
        else
        {
            score += i;
        }

        /** 현재 보드 출력 */
        print_board(input, score);
    }

    return 0;
}

void create(int num)
{ // cout << "create 함수 구현\n";
    // 빈 칸에 특정 숫자 생성
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<int> dis(0, BOARD_SIZE * BOARD_SIZE - 1);
    int random = dis(gen);

    while (true)
    { // 빈 칸을 찾을 때까지 반복
        if (board[random / BOARD_SIZE][random % BOARD_SIZE] == 0)
        {                                        // 빈 칸이면
            board[random / BOARD_SIZE][random % BOARD_SIZE] = num; // 특정 숫자 생성
            break;
        }
        else
        { // 빈 칸이 아니면 다시 랜덤으로 생성
            random = dis(gen);
        }
    }
}

bool is_full()
{ // cout << "is_full 함수 구현\n";
    for (int i = 0; i < BOARD_SIZE; i++)
    {
        for (int j = 0; j < BOARD_SIZE; j++)
        {
            if (board[i][j] == 0)
            {
                return false; // 보드가 하나라도 비어있으면 false 반환
            }
        }
    }
    // 보드가 전부 차있으면 true 반환
    return true;
}

int random_create()
{ // cout << "random_create 함수 구현\n";
    // random_create로 80% 확률로 2, 20% 확률로 4 생성
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<int> dis(0, 4);
    int random = dis(gen);

    if (is_full())
    { // 보드가 가득차면 -1 반환
        return -1;
    }
    else if (random == 0)
    { // 20% 확률로 4 생성
        create(4);
        return 4;
    }
    else
    { // 80% 확률로 2 생성
        create(2);
        return 2;
    }
}

void write_line()
{ // cout << "write_line 함수 구현\n";
    for (int i = 0; i < (BOARD_SIZE * 8) + 1; i++)
    { // BOARD_SIZE = 4일 때 33. 1당 8.
        cout << "-";
    }
    cout << "\n";
}

void print_board(string input, int score)
{ // cout << "print_board 함수 구현\n";
    // 현재 보드 출력
    cout << "input: " << input << "\n";
    cout << "score: " << score << "\n";
    write_line();
    for (int i = 0; i < BOARD_SIZE; i++)
    {
        cout << "|";
        for (int j = 0; j < BOARD_SIZE; j++)
        {
            cout << "\t" << board[i][j] << "\t|";
        }
        cout << "\n";
        write_line();
    }
}

void up()
{ // cout << "up 함수 구현\n";
    // 칸이 0이면 0이 아닌 아래의 가장 위 블록을 자신 위치로
    // 칸이 0이 아니면 자신과 같은 숫자의 아래의 가장 위 블록을 자신 위치로

    // 각 세로줄에 대해 위로 밀기
    for (int j = 0; j < BOARD_SIZE; j++)
    {
        for (int i = 0; i < BOARD_SIZE - 1; i++)
        { // 위부터 차례로 탐색. 마지막 칸은 필요 없음
            if (board[i][j] == 0)
            { // 빈 칸이 있으면
                for (int k = i + 1; k < BOARD_SIZE; k++)
                { // 빈 칸 아래에 있는 숫자를 찾음
                    if (board[k][j] != 0)
                    {                              // 숫자가 있으면
                        board[i][j] = board[k][j]; // 위로 끌어올림
                        board[k][j] = 0;
                        i--; // 다시 자신의 위치부터 탐색.
                        break;
                    }
                }
            }
            else
            { // 채워져 있는 블록인 경우
                for (int k = i + 1; k < BOARD_SIZE; k++)
                { // 빈 칸 아래에 있는 숫자를 찾음
                    if (board[k][j] != 0)
                    { // 숫자가 있으면
                        if (board[i][j] == board[k][j])
                        { // 같은 숫자면 합침
                            board[i][j] *= 2;
                            board[k][j] = 0;
                        }
                        break;
                    }
                }
            }
        }
    }
}

void down()
{ // cout << "down 함수 구현\n";
    // 칸이 0이면 0이 아닌 위의 가장 아래 블록을 자신 위치로
    // 칸이 0이 아니면 자신과 같은 숫자의 위의 가장 아래 블록을 자신 위치로

    // 각 세로줄에 대해 아래로 밀기
    for (int j = 0; j < BOARD_SIZE; j++)
    {
        for (int i = BOARD_SIZE - 1; i > 0; i--)
        { // 아래부터 차례로 탐색. 첫 번째 칸은 필요 없음
            if (board[i][j] == 0)
            { // 빈 칸이 있으면
                for (int k = i - 1; k >= 0; k--)
                { // 빈 칸 위에 있는 숫자를 찾음
                    if (board[k][j] != 0)
                    {                              // 숫자가 있으면
                        board[i][j] = board[k][j]; // 아래로 끌어내림
                        board[k][j] = 0;
                        i++; // 다시 자신의 위치부터 탐색.
                        break;
                    }
                }
            }
            else
            { // 채워져 있는 블록인 경우
                for (int k = i - 1; k >= 0; k--)
                { // 빈 칸 위에 있는 숫자를 찾음
                    if (board[k][j] != 0)
                    { // 숫자가 있으면
                        if (board[i][j] == board[k][j])
                        { // 같은 숫자면 합침
                            board[i][j] *= 2;
                            board[k][j] = 0;
                        }
                        break;
                    }
                }
            }
        }
    }
}

void left()
{ // cout << "left 함수 구현\n";
    // 칸이 0이면 0이 아닌 오른쪽의 가장 왼쪽 블록을 자신 위치로
    // 칸이 0이 아니면 자신과 같은 숫자의 오른쪽의 가장 왼쪽 블록을 자신 위치로

    // 각 가로줄에 대해 왼쪽으로 밀기
    for (int i = 0; i < BOARD_SIZE; i++)
    {
        for (int j = 0; j < BOARD_SIZE - 1; j++)
        { // 왼쪽부터 차례로 탐색. 마지막 칸은 필요 없음
            if (board[i][j] == 0)
            { // 빈 칸이 있으면
                for (int k = j + 1; k < BOARD_SIZE; k++)
                { // 빈 칸 오른쪽에 있는 숫자를 찾음
                    if (board[i][k] != 0)
                    {                              // 숫자가 있으면
                        board[i][j] = board[i][k]; // 왼쪽으로 끌어옴
                        board[i][k] = 0;
                        j--; // 다시 자신의 위치부터 탐색.
                        break;
                    }
                }
            }
            else
            { // 채워져 있는 블록인 경우
                for (int k = j + 1; k < BOARD_SIZE; k++)
                { // 빈 칸 오른쪽에 있는 숫자를 찾음
                    if (board[i][k] != 0)
                    { // 숫자가 있으면
                        if (board[i][j] == board[i][k])
                        { // 같은 숫자면 합침
                            board[i][j] *= 2;
                            board[i][k] = 0;
                        }
                        break;
                    }
                }
            }
        }
    }
}

void right()
{ // cout << "right 함수 구현\n";
    // 칸이 0이면 0이 아닌 왼쪽의 가장 오른쪽 블록을 자신 위치로
    // 칸이 0이 아니면 자신과 같은 숫자의 왼쪽의 가장 오른쪽 블록을 자신 위치로

    // 각 가로줄에 대해 오른쪽으로 밀기
    for (int i = 0; i < BOARD_SIZE; i++)
    {
        for (int j = BOARD_SIZE - 1; j > 0; j--)
        { // 오른쪽부터 차례로 탐색. 첫 번째 칸은 필요 없음
            if (board[i][j] == 0)
            { // 빈 칸이 있으면
                for (int k = j - 1; k >= 0; k--)
                { // 빈 칸 왼쪽에 있는 숫자를 찾음
                    if (board[i][k] != 0)
                    {                              // 숫자가 있으면
                        board[i][j] = board[i][k]; // 오른쪽으로 끌어옴
                        board[i][k] = 0;
                        j++; // 다시 자신의 위치부터 탐색.
                        break;
                    }
                }
            }
            else
            { // 채워져 있는 블록인 경우
                for (int k = j - 1; k >= 0; k--)
                { // 빈 칸 왼쪽에 있는 숫자를 찾음
                    if (board[i][k] != 0)
                    { // 숫자가 있으면
                        if (board[i][j] == board[i][k])
                        { // 같은 숫자면 합침
                            board[i][j] *= 2;
                            board[i][k] = 0;
                        }
                        break;
                    }
                }
            }
        }
    }
}