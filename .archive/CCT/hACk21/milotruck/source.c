#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
char soup[50];
int milo = 100000;
int milotruck = 100000;
#define clear() printf("\033[H\033[J")
void initialise(){
	// Unimportant Initialisation
    strcpy( soup, "cat flag" );
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	// Print Banner
	printf(".___  ___.  __   __        ______   .___________..______       __    __    ______  __  ___\n |   \/   | |  | |  |      /  __  \  |           ||   _  \     |  |  |  |  /      ||  |/  / \n |  \  /  | |  | |  |     |  |  |  | `---|  |----`|  |_)  |    |  |  |  | |  ,----'|  '  /  \n |  |\/|  | |  | |  |     |  |  |  |     |  |     |      /     |  |  |  | |  |     |    <   \n |  |  |  | |  | |  `----.|  `--'  |     |  |     |  |\  \----.|  `--'  | |  `----.|  .  \  \n |__|  |__| |__| |_______| \______/      |__|     | _| `._____| \______/   \______||__|\__\ \n\n");
    printf("                       _____________________________________________________\n             _______  |                      _ _                            | \n            / _____ | |                     (_) |                           |\n           / /(__) || |            _ __ ___  _| | ___                       | \n  ________/ / |OO| || |           | '_ ` _ \| | |/ _ \                      | \n |         |-------|| |           | | | | | | | | (_) |                     | \n |         |       || |           |_| |_| |_|_|_|\___/                      | \n(|         |     -.|| |_______________________                              | \n |  ____   \       ||_________||____________  |             ____      ____  | \n/| / __ \   |______||     / __ \   / __ \   | |            / __ \    / __ \ |\ \n\|| /  \ |_______________| /  \ |_| /  \ |__| |___________| /  \ |__| /  \|_|/ \n   | () |                 | () |   | () |                  | () |    | () | \n    \__/                   \__/     \__/                    \__/      \__/");
	sleep(1);
	clear();
}
void print_menu(){
	// Show Current State
	printf("Milo in Milotruck: %d.%02d\n", milotruck/100, milotruck%100);
	printf("Milo you have:     %d.%02d\n", milo/100, milo%100);
	puts("");
	// Show Options
	printf("1) Contribute milo to milotruck!!\n2) Squeeze milo out of milotruck\n3) Buy wealthy-turtle soup\n4) Quit\n\n");
    printf("I heard its even possible to squeeze out horlicks from milotruck....\n5) Horlicks\n\n");
}
void contribute(){
	int amount;
	printf("How much MILO (ml) would you like to CONTRIBUTE?\n");
	printf("> ");
	scanf("%d", &amount);
	if(amount * 100 < milo){
		milo  -= amount * 100;
		milotruck += amount * 100;
	}
	else{
		// Insufficient funds in wallet
		printf("[-] Error: You do not have sufficient milo to CONTRIBUTE\n");
	}
}
void squeeze(){
	int amount;
	printf("How much MILO (ml) would you like to SQUEEZE?\n");
	printf(" ");
	scanf("%d", &amount);
	if(amount * 100 < milotruck){
		milotruck -= amount * 100;
		milo  += amount * 100;
	}
	else{
		printf("[-] Error: You do not have sufficient MILO to SQUEEZE\n");
	}
}
void flag(const char *command){
	if(milo > 31333700){
		milo -= 31337000;
		system(command);
		exit(0);
	}
	else{
		printf("[-] Error: You cannot buy the recipe for wealthy-turtle soup. Come back when you have 313337.00 ml of MILO\n");
	}
}
void horlicks(){
    printf("How much horlicks can you squeeze out of milotruck??\n");
    printf("Nahhhhhhhhhhhhhhhhhhhhhhhhh\n");
    printf(" ");
    scanf("%s", &soup);
    
}
int get_choice(){
	print_menu();
	int choice;
	printf("Your choice: ");
	scanf("%d", &choice);
	puts("");
	return choice;
}
int main(){
	initialise();
	for(;;){
		switch(get_choice()){
			case 1:
				contribute();
				break;
			case 2:
				squeeze();
				break;
			case 3:
				flag(soup);
				break;
			case 4:
				return 0;
            case 5:
                horlicks();
                break;
			default:
				printf("[-] Invalid choice\n");
		}
		puts("");
	}
}