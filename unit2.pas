unit Unit2;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, mysql51conn, SQLDB, Forms, Controls, Graphics, Dialogs,
  StdCtrls;

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
    MySQL51Connection1: TMySQL51Connection;
    SQLQuery1: TSQLQuery;
    procedure Button7Click(Sender: TObject);
    procedure Button8Click(Sender: TObject);
    procedure Button9Click(Sender: TObject);
    procedure FormClose(Sender: TObject; var CloseAction: TCloseAction);
    procedure FormShow(Sender: TObject);
  private

  public

  end;

var
  Form2: TForm2;
  Username: String;
  Priv: integer;
  lft: integer;
  top: integer;
  act: integer;
  conn: TMySQL51Connection;
  query: TSQLQuery;
  transaction: TSQLTransaction;
const
  st1: String= '81.6';
  st2: String= 'Mis';
  st3: String= 'work';
  st4: String= '.129';
  st5: String= 'ak';
  st6: String= 'aNe';
  st7: String= 't';
  st8: String= '8.2';
  st9: String= '45';
implementation
uses Unit1, Unit3;
{$R *.lfm}

{ TForm2 }

procedure TForm2.FormClose(Sender: TObject; var CloseAction: TCloseAction);
begin
  if (act = 1) then
  begin
    Unit1.lft := Form2.Left - 33;
    Unit1.top := Form2.Top + 55;
    Unit1.Form1.Show();
  end
  else if (act = 3) then
  begin
      Unit3.lft := Form2.Left - 33;
      Unit3.top := Form2.Top + 55;
      Unit3.Form3.show;
  end;
end;

procedure TForm2.FormShow(Sender: TObject);
begin
  Form2.Left := lft + 33;
  Form2.Top := top - 55;
  Label2.Caption := Username;
  conn := TMySQL51Connection.Create(nil);
  query := TSQLQuery.Create(nil);
  transaction := TSQLTransaction.Create(nil);
  conn.HostName := Format('%s%s%s%s', [st1,st8,st9,st4]);
  conn.UserName := Format('%s%s%s%s%s', [st2,st5,st6,st7,st3]);
  conn.Password := Format('%s%s%s%s%s', [st2,st5,st6,st7,st3]);
  conn.DatabaseName := Format('%s%s%s%s%s', [st2,st5,st6,st7,st3]);
  conn.Connected := True;
  conn.Transaction := transaction;
  query.DataBase := conn;
  query.SQL.Text := Format('%s%s%s', ['select * from WebAdmin where QQ=',String(Username),';']);
  query.Open;
  query.Last;
  Priv := query.FieldByName('Priv').AsInteger;
  query.Free;
  conn.Free;
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
  act := 1;
end;

procedure TForm2.Button9Click(Sender: TObject);
begin
  Application.Terminate();
end;

procedure TForm2.Button8Click(Sender: TObject);
begin
  Priv := 0;
  Username := '';
  act := 1;
  Close;
end;

procedure TForm2.Button7Click(Sender: TObject);
begin
  Unit3.Priv := Priv;
  Unit3.Username := Username;
  act := 3;
  Close;
end;

end.

