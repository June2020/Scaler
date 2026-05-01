package com.tunemate

import android.app.Application
import org.koin.android.ext.koin.androidContext
import org.koin.core.context.startKoin

class TuneMateApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        startKoin {
            androidContext(this@TuneMateApplication)
            modules(emptyList())  // DI module added in Task 12
        }
    }
}
