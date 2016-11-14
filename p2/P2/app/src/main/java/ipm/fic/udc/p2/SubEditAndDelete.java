package ipm.fic.udc.p2;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
;

public class SubEditAndDelete extends AppCompatActivity implements OnClickListener{


    /**
     * Atributos
     */

    private EditText etM;
    private Button bEdit, bDelete, bCancel;
    private int posM;
    private Bundle extras;
    private String name;
    private boolean editedC;


    /**
     * Metodos
     */

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {

        super.onCreate(savedInstanceState);

        setContentView(R.layout.modify_main);

        extras = getIntent().getExtras();
        posM = extras.getInt("posE");
        name = extras.getString("name");
        editedC = extras.getBoolean("editedA");

        etM = (EditText) findViewById(R.id.txM);
        etM.setHint(name);
        bEdit = (Button) findViewById(R.id.btEdit);
        bDelete = (Button) findViewById(R.id.btDelete);
        bCancel = (Button) findViewById(R.id.btCancel);

        name = "";

        bEdit.setOnClickListener(this);
        bDelete.setOnClickListener(this);
        bCancel.setOnClickListener(this);

    }


    @Override
    public void onClick(View v)
    {

        switch (v.getId()) {
            case R.id.btEdit:
                editedC = true;
                name = etM.getText().toString();
                etM.setText("");
                this.returnHome();
                break;

            case R.id.btDelete:
                editedC = true;
                etM.setText("");
                this.returnHome();
                break;

            case R.id.btCancel:
                etM.setText("");
                posM = -1;
                this.returnHome();
                break;
        }
    }


    public void returnHome() {
        Intent intent = new Intent();
        intent.putExtra("nameE",name);
        intent.putExtra("posD", posM);
        intent.putExtra("editedC", editedC);
        setResult(RESULT_OK,intent);
        super.finish();
    }


}