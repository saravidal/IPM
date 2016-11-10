package ipm.fic.udc.p2;


import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;


public class SubAddActivity extends AppCompatActivity implements OnClickListener{


    /**
     * Atributos
     */

    private EditText txAdd;
    private Button bAdd;
    private Button bCancel;
    private String name;


    /**
     * Metodos
     */

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.add_main);

        txAdd = (EditText) findViewById(R.id.txAdd);
        bAdd = (Button) findViewById(R.id.btAdd);
        bCancel = (Button) findViewById(R.id.btCancel);

        name = "";

        bAdd.setOnClickListener(this);
        bCancel.setOnClickListener(this);
    }


    @Override
    public void onClick(View v)
    {
        switch (v.getId()) {

            case R.id.btAdd:
                name = txAdd.getText().toString();
                txAdd.setText("");
                this.returnHome();
                break;

            case R.id.btCancel:
                txAdd.setText("");
                this.returnHome();
                break;
        }
    }


    public void returnHome() {
        Intent intent = new Intent();
        intent.putExtra("nameE", name);
        setResult(RESULT_OK,intent);
        super.finish();
    }


}