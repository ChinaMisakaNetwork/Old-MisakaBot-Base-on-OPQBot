program project1;

{$mode objfpc}{$H+}

uses
  {$IFDEF UNIX}{$IFDEF UseCThreads}
  cthreads,
  {$ENDIF}{$ENDIF}
  Interfaces, // this includes the LCL widgetset
  Forms, Unit1, Unit2, Unit3
  { you can add units after this };

{$R *.res}

begin
  RequireDerivedFormResource:=True;
  Application.Scaled:=True;
  Application.Initialize;
  Application.CreateForm(TForm1, Form1);
  Application.CreateForm(TForm2, Form2);
  Application.CreateForm(TForm3, Form3);
  Unit1.Form1.ShowInTaskbar := stAlways;
  Unit2.Form2.ShowInTaskbar := stAlways;
  Unit3.Form3.ShowInTaskbar := stAlways;
  Unit1.lft := 659;
  Unit1.top := 348;
  Application.Run;
end.

