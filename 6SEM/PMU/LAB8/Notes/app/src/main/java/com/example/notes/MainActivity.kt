package com.example.notes

import android.os.Bundle
import android.view.View.OnCreateContextMenuListener
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.ViewModelProvider
import com.example.notes.database.NoteDatabase
import com.example.notes.repository.NoteRepository
import com.example.notes.viewmodel.NoteViewModel
import com.example.notes.viewmodel.NoteViewModelFactory

class MainActivity : AppCompatActivity() {

    lateinit var noteViewModel: NoteViewModel

        override fun onCreate(savedInstanceState: Bundle?){
            super.onCreate(savedInstanceState)
            setContentView(R.layout.activity_main)

            setupViewModel()


        }




        private fun setupViewModel(){
            val noteRepository = NoteRepository(NoteDatabase( this))
            val viewModelProviderFactory = NoteViewModelFactory(application, noteRepository)
            noteViewModel = ViewModelProvider( this, viewModelProviderFactory) [NoteViewModel::class.java ]



        }

}