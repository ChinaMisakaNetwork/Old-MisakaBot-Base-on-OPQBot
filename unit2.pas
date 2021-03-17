unit Unit2;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls;

type

  { TForm2 }

  TForm2 = class(TForm)
    Button1: TButton;
    Button2: TButton;
    Button3: TButton;
    Button4: TButton;
    Button5: TButton;
    Button6: TButton;
    Button7: TButton;
    Button8: TButton;
    Button9: TButton;
    Label1: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    procedure Button8Click(Sender: TObject);
    procedure Button9Click(Sender: TObject);
    procedure FormClose(Sender: TObject; var CloseAction: TCloseAction);
    procedure FormShow(Sender: TObject);
  private

  public

  end;

var
  Form2: TForm2;
  Username: integer;
  Priv: integer;
implementation
uses Unit1;
{$R *.lfm}

{ TForm2 }

procedure TForm2.FormClose(Sender: TObject; var CloseAction: TCloseAction);
begin
  Unit1.Form1.Show();
end;

procedure TForm2.FormShow(Sender: TObject);
begin
  Label2.Caption := IntToStr(Username);
  if (((Priv div 4) mod 2) = 1) then
  begin
    Button1.Enabled := true;
    Button2.Enabled := true;
  end
  else
  begin
    Button1.Enabled := false;
    Button2.Enabled := false;
  end;
  if (((Priv div 2) mod 2) = 1) then
  begin
    Button3.Enabled := true;
    Button4.Enabled := true;
    Button5.Enabled := true;
  end
  else
  begin
    Button3.Enabled := false;
    Button4.Enabled := false;
    Button5.Enabled := false;
  end;
  if (((Priv) mod 2) = 1) then
  begin
    Button6.Enabled := true;
  end
  else
  begin
    Button6.Enabled := false;
  end;
end;

procedure TForm2.Button9Click(Sender: TObject);
begin
  Application.Terminate();
end;

procedure TForm2.Button8Click(Sender: TObject);
begin
  Priv := 0;
  Username := 0;
end;

end.

