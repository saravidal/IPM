package ipm.fic.udc.p2;


import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import java.util.ArrayList;


public class MainEditAndDelete extends AppCompatActivity implements OnClickListener{


    /**
     * Atributos
     */

    private EditText etM;
    private Button bEdit, bDelete, bCancel;
    private int posMn, posMa;

    private Category category = new Category();

    private Bundle extras;
    private String categoryname;
    private ArrayList<String> names;


    /**
     * Metodos
     */

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {

        super.onCreate(savedInstanceState);

        setContentView(R.layout.modify_main);

        extras = getIntent().getExtras();
        posMn = extras.getInt("posAn");
        posMa = extras.getInt("posAa");
        categoryname = extras.getString("categoryName");
        names = extras.getStringArrayList("nameslist");

        etM = (EditText) findViewById(R.id.txM);
        etM.setHint(categoryname);
        bEdit = (Button) findViewById(R.id.btEdit);
        bDelete = (Button) findViewById(R.id.btDelete);
        bCancel = (Button) findViewById(R.id.btCancel);

        category.setName("");
        category.setSublist(extras.getStringArrayList("categorysublist"));

        bEdit.setOnClickListener(this);
        bDelete.setOnClickListener(this);
        bCancel.setOnClickListener(this);

    }


    @Override
    public void onClick(View v)
    {

        switch (v.getId()) {
            case R.id.btEdit:
                category.setName(etM.getText().toString());
                if (search(names,category.getName()) == false) {
                    etM.setText("");
                    this.returnHome();
                    break;
                }
                else{
                    category.setName("");
                    Toast.makeText(getApplicationContext(),
                            R.string.already_exists_toast, Toast.LENGTH_LONG).show();
                    break;
                }

            case R.id.btDelete:
                etM.setText("");
                this.returnHome();
                break;

            case R.id.btCancel:
                etM.setText("");
                posMa = -1;
                this.returnHome();
                break;
        }
    }


    public void returnHome() {
        Intent intent = new Intent();
        intent.putExtra("categoryD",category);
        intent.putExtra("posDn", posMn);
        intent.putExtra("posDa", posMa);
        setResult(RESULT_OK,intent);
        super.finish();
    }


    private boolean search (ArrayList<String> array, String name) {
        int i;
        boolean result = false;

        for (i = 0; i < array.size(); i++) {
            if (array.get(i).compareTo(name) == 0) {
                result = true;
                break;
            }
        }

        return result;
    }


}