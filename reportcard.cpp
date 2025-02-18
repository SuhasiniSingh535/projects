#include<iostream>//for input and output
#include<fstream>//for file handling
#include<windows.h>//for some specific path
#define size 5
using namespace std;
class reportcard
{
	private:int maxmarksT[size];
			int obtmarksT[size];
			int maxmarksP[size];
			int obtmarksP[size];
			
	public:
		reportcard()
		{
			
			int i;
			for(i=0;i<=size;i++)
			{
				maxmarksT[i]=100;
			}
			for(i=0;i<=size;i++)
			{
				obtmarksT[i]=0;
			}
			for(i=0;i<=size;i++)
			{
				maxmarksP[i]=50;
			}
			for(i=0;i<=size;i++)
			{
				obtmarksP[i]=0;
			}
		}
		
		void input()
		{
			int i;
			cout<<"enter the obtained marks of theory subjects:";
			for(i=0;i<=size;i++)
			{
				cin>>obtmarksT[i];
			}
			cout<<"enter the obtained of practical subjects:";
			for(i=0;i<=size;i++)
			{
				cin>>obtmarksP[i];
			}
		}
		void display()
		{
			int i;
			cout<<"Maximum marks in theory subjects are:";
			for(i=0;i<=size;i++)
			{
				cout<<"\t"<<maxmarksT[i];
			}
			cout<<"\n";
			cout<<"obtained marks in theory subjects are:";
			for(i=0;i<=size;i++)
			{
				cout<<"\t"<<obtmarksT[i];
			}
			cout<<"\n";
			cout<<"Maximum marks in practical subjects are:";
			for(i=0;i<=size;i++)
			{
				cout<<"\t"<<maxmarksP[i];
			}
			cout<<"\n";
			cout<<"obtained marks in practical subjects are:";
			for(i=0;i<=size;i++)
			{
				cout<<"\t"<<obtmarksP[i];
			}
			cout<<"\n";
		}
		float findper()
		{
			float sum1,sum2;
			int i;
			sum1=sum2=0;
			for(i=0;i<=size;i++)
			{
				sum1=sum1+obtmarksT[i]+obtmarksP[i];
				sum2=sum2+maxmarksT[i]+maxmarksP[i];
			}
			cout<<"\ntotal marks obtained in theory and practical="<<sum1;
			cout<<"\n";
			cout<<"\ntotal maximam marks of tehory and practical="<<sum2;
			cout<<"\n";
			return (sum1*100)/sum2;
		}
		void findgrade(float percentage)
		{
			if(percentage<23)
			{
				cout<<"\fail";
				cout<<"\n";
			}
			
			else if(33<percentage && percentage<=48)
			{
				cout<<"\n 3rd division";
				cout<<"\n";
			}
			
			else if(49<percentage && percentage<=59)
			{
				cout<<"\n 2nd divison";
				cout<<"\n";
			}
			
			else if(60<percentage && percentage<=74)
			{
				cout<<"\n 1st divison";
				cout<<"\n";
			}
			
			else
			{
				cout<<"\n distintion";
				cout<<"\n";
			}
			
		}
};
int main()
{
	reportcard R;
	float percentage;
	R.input();
	R.display();
	percentage=R.findper();
	cout<<"\n";
	cout<<"\n percentage="<<percentage<<"%";
	R.findgrade(percentage);
	return 0;
}


